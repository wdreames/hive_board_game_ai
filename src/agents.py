from abc import abstractmethod
from timeit import default_timer as timer
import src.game.board as board
import src.game.spaces as spaces
import src.utils as utils
import random
from tqdm import tqdm


class Agent:

    def __init__(self, is_white=True, board_manager=None):
        if board_manager is None:
            board_manager = board.BoardManager()

        self.is_white = is_white
        self.board_manager = board_manager
        self.actions_performed = []

        self.name = 'Agent'

    def get_action(self):
        chosen_action = self.get_action_selection()
        self.actions_performed.append(chosen_action)
        self.board_manager.reset_board()
        return chosen_action

    def get_evaluation(self):
        # Base evaluation of the board state
        evaluation = self.board_manager.get_board().evaluate_state()
        if not self.is_white:
            evaluation *= -1

        return evaluation

    @abstractmethod
    def get_action_selection(self):
        pass

    def __str__(self):
        return f'{self.name} ({"White" if self.is_white else "Black"})'


# TODO: Rename to DebugPlayer
class Player(Agent):

    def __init__(self, is_white=True, board_manager=None):
        super().__init__(is_white, board_manager)
        self.name = 'Player'

    def get_action_selection(self):
        actions = self.board_manager.get_action_list()

        if len(actions) == 1 and actions[0][0] == board.HiveGameBoard.SKIP_TURN:
            print('You have no legal moves. Skipping turn...')
            return actions[0]

        return utils.make_choice(
            'The following actions can be played:',
            'Select an action:',
            actions
        )


# TODO: Rename to Player
class HexPlayer(Agent):

    def __init__(self, is_white=True, board_manager=None):
        super().__init__(is_white, board_manager)
        self.name = 'Player'

    # TODO: Refactor this function. It's really messy...
    def get_action_selection(self):
        print()

        pieces_to_play, locations_to_place, possible_moves_dict = self.board_manager.get_board().get_all_possible_actions()
        ui_id_to_coords = self.board_manager.get_board().ui_id_to_coords
        ui_coords_to_id = self.board_manager.get_board().ui_coords_to_id

        has_legal_placements = locations_to_place and sum([amount for amount in pieces_to_play.values()]) > 0
        has_legal_movements = len(possible_moves_dict) > 0

        cancel_action = 'Cancel action'

        # Tell the player which pieces they can place
        if has_legal_placements:
            print('You have the following pieces in your reserve:')
            for piece_type, amount in pieces_to_play.items():
                if amount:
                    print(f'\t* {piece_type} x {amount}')

        # Tell the player which pieces they can move
        if has_legal_movements:
            print('You can move the following pieces on the board (represented by their number ID):')
            for piece_location in possible_moves_dict.keys():
                if piece_location in ui_coords_to_id:
                    print(f'\t* {ui_coords_to_id[piece_location]}')

        # Determine if the player is placing or moving a piece
        if has_legal_placements and has_legal_movements:
            action_type = utils.make_choice(
                'Do you want to place a piece or move a piece?',
                'Select an action type:',
                [board.HiveGameBoard.PLACE_PIECE, board.HiveGameBoard.MOVE_PIECE]
            )
        elif has_legal_placements:
            action_type = board.HiveGameBoard.PLACE_PIECE
        elif has_legal_movements:
            action_type = board.HiveGameBoard.MOVE_PIECE
        else:
            action_type = board.HiveGameBoard.SKIP_TURN

        # Player places a piece
        if action_type == board.HiveGameBoard.PLACE_PIECE:
            piece_options = []
            for type_of_piece, amount in pieces_to_play.items():
                if amount:
                    piece_options.append(type_of_piece)
            piece_options.append(cancel_action)

            # Player chooses a piece to place
            piece_type = utils.make_choice(
                'Which type of piece would you like to place?',
                'Select a type of piece:',
                piece_options
            )
            if piece_type == cancel_action:
                return self.get_action_selection()

            # Player chooses a location to place a piece
            location_options = []
            for coordinate in locations_to_place:
                if coordinate in ui_coords_to_id:
                    location_options.append(ui_coords_to_id[coordinate])
            location_options.sort()
            location_options.append(cancel_action)
            location_number = utils.make_choice(
                f'Where would you like to place a new {piece_type}?',
                'Select a location (represented by number ID):',
                location_options
            )
            if location_number == cancel_action:
                return self.get_action_selection()

            chosen_action = (action_type, ui_id_to_coords[location_number], piece_type)

        # Player moves a piece
        elif action_type == board.HiveGameBoard.MOVE_PIECE:
            # Player chooses a piece to move
            piece_locations = []
            for coordinate in possible_moves_dict.keys():
                if coordinate in ui_coords_to_id:
                    piece_locations.append(ui_coords_to_id[coordinate])
            piece_locations.sort()
            piece_locations.append(cancel_action)
            location_number = utils.make_choice(
                'Which piece would you like to move?',
                'Select a piece (represented by number ID):',
                piece_locations
            )
            if location_number == cancel_action:
                return self.get_action_selection()

            piece_location = ui_id_to_coords[location_number]
            piece_moves = possible_moves_dict[piece_location]

            # Player chooses where to move their piece
            new_locations = []
            for coordinate in piece_moves:
                if coordinate in ui_coords_to_id:
                    new_locations.append(ui_coords_to_id[coordinate])
            new_locations.sort()
            new_locations.append(cancel_action)
            new_location_number = utils.make_choice(
                f'Where would you like to move the piece at {location_number}',
                'Select a space on the board (represented by number ID):',
                new_locations
            )
            if new_location_number == cancel_action:
                return self.get_action_selection()
            new_location = ui_id_to_coords[new_location_number]

            chosen_action = (board.HiveGameBoard.MOVE_PIECE, piece_location, new_location)

        # Player has no legal actions - skip their turn.
        else:
            print('You have no legal moves. Skipping turn...')
            chosen_action = (board.HiveGameBoard.SKIP_TURN, None, None)

        return chosen_action


class RandomActionAI(Agent):

    def __init__(self, is_white=True, board_manager=None):
        super().__init__(is_white, board_manager)
        self.name = 'Random Action AI'

    def get_action_selection(self):
        actions = self.board_manager.get_action_list()
        rand_index = random.randint(0, len(actions) - 1)
        return actions[rand_index]


class BestNextMoveAI(Agent):

    def __init__(self, is_white=True, board_manager=None, winning_value=50000):
        super().__init__(is_white, board_manager)
        self.name = 'Best Next Move AI'
        self.winning_value = winning_value

    def get_action_selection(self):
        actions = self.board_manager.get_action_list()

        # For every action, get the board's successive state and its evaluation
        # Choose a random action out of those with the highest evaluation

        best_evaluation = -float("inf")
        best_actions = []
        for i, action in enumerate(actions):
            self.board_manager.get_successor(action)
            evaluation = self.get_evaluation()
            self.board_manager.get_predecessor()

            if evaluation >= self.winning_value:
                return action
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_actions.clear()
            if evaluation >= best_evaluation:
                best_actions.append(action)

        return random.choice(best_actions)


class MinimaxAI(Agent):

    def __init__(self, is_white=True, board_manager=None, max_depth=4, max_time=float("inf"), winning_value=10000):
        super().__init__(is_white, board_manager)
        self.max_depth = max_depth if max_depth >= 1 else 1
        self.max_time = max_time if max_time > 0 else 1
        self.name = f'Minimax AI with Depth {self.max_depth}'
        self.winning_value = winning_value
        self.start_location = None
        self.sorted_action_lists = dict()
        self.maximizing = 'max'
        self.minimizing = 'min'

    def get_opening_move(self, actions, action_number):
        if action_number == 1:
            possible_pieces_to_place = [spaces.Piece.SPIDER, spaces.Piece.GRASSHOPPER, spaces.Piece.BEETLE]
        elif action_number == 2:
            placed_piece = None
            if self.is_white:
                for piece, amount in self.board_manager.get_board().num_white_free_pieces.items():
                    if amount:
                        placed_piece = piece
                        break
            if not self.is_white:
                for piece, amount in self.board_manager.get_board().num_black_free_pieces.items():
                    if amount:
                        placed_piece = piece
                        break

            if placed_piece == spaces.Piece.GRASSHOPPER or placed_piece == spaces.Piece.BEETLE:
                possible_pieces_to_place = [spaces.Piece.ANT]
            else:
                possible_pieces_to_place = [spaces.Piece.GRASSHOPPER, spaces.Piece.ANT]
        else:
            return None

        random_piece = random.choice(possible_pieces_to_place)
        random_action = actions.pop()

        if action_number == 1:
            self.start_location = random_action[1]

        return random_action[0], random_action[1], random_piece

    def get_action_selection(self):
        # Check if we have seen this list of actions before
        action_list = tuple(self.board_manager.get_action_list())
        if action_list in self.sorted_action_lists:
            actions, max_or_min = self.sorted_action_lists[action_list]
            if max_or_min != self.maximizing:
                actions.reverse()
        else:
            actions = list(action_list)

        # Opening moves
        action_number = (self.board_manager.get_board().turn_number + 1) // 2
        if action_number <= 2:
            chosen_action = self.get_opening_move(actions, action_number)
            if chosen_action is not None:
                return chosen_action
        elif action_number <= 4:
            better_action_list = []

            possible_locations = self.board_manager.get_board().pieces[self.start_location].get_all_surrounding_locations()

            for action in actions:
                # Don't place Beetles or Spiders
                if action[2] not in [spaces.Piece.BEETLE, spaces.Piece.SPIDER] and \
                        action[1] in possible_locations:
                    better_action_list.append(action)
            if better_action_list:
                actions = better_action_list

        # If there is only one move, play it
        if len(actions) == 1:
            return actions.pop()

        # Run iterative deepening
        start_time = timer()
        action_evaluations = dict()
        for d in range(self.max_depth):
            alpha = -self.winning_value
            beta = self.winning_value

            # Check all the actions with maximum depth, d
            with tqdm(total=len(actions)) as pbar:
                for i, action in enumerate(actions):
                    next_board_state = self.board_manager.get_successor(action)
                    action_eval = self.min_value(next_board_state, alpha, beta, (d * 2) + 1, start_time)
                    self.board_manager.get_predecessor()

                    # Check if time has run out
                    if action_eval is None and action not in action_evaluations:
                        action_evaluations[action] = -self.winning_value
                    if action_eval is None or timer() - start_time >= self.max_time:
                        # Return the best action that was found
                        actions = [action for action, value in sorted(action_evaluations.items(), key=lambda x: -x[1])]
                        return self._select_best_from_actions(actions, action_evaluations)

                    # If a winning move was found, play it
                    if action_eval >= self.winning_value:
                        return action

                    # Store evaluation
                    action_evaluations[action] = action_eval
                    alpha = max(alpha, action_eval)

                    pbar.update()

            # Sort the action list based on the evaluations found during this iteration (high to low)
            actions = [action for action, value in sorted(action_evaluations.items(), key=lambda x: -x[1])]
            self.sorted_action_lists[action_list] = actions, self.maximizing

            # If every action is a losing move, return a random action.
            if action_evaluations[actions[0]] <= -self.winning_value:
                return random.choice(actions)

            # If a forced win was found, exit the loop to return the best move
            if action_evaluations[actions[0]] >= self.winning_value - 1:
                break

        return self._select_best_from_actions(actions, action_evaluations)

    @staticmethod
    def _select_best_from_actions(action_list, action_evaluations):
        # Assumes action_list is already sorted based on evaluations high to low
        best_value = action_evaluations[action_list[0]]
        best_actions = []
        for action in action_list:
            if action_evaluations[action] >= best_value:
                best_actions.append(action)
            else:
                break

        return random.choice(best_actions)

    def max_value(self, board_state, alpha, beta, depth, start_time):
        if board_state.determine_winner() is not None:
            return self.get_evaluation()
        elif self.find_win(board_state, white_to_move=self.is_white):
            # Found a forced win, but returning (winning_value - 1) in case there is a faster win
            return self.winning_value - 1
        elif depth <= 0:
            return self.get_evaluation()

        # Check if we have seen this list of actions before
        action_list = tuple(board_state.get_action_list())
        if action_list in self.sorted_action_lists:
            actions, max_or_min = self.sorted_action_lists[action_list]
            if max_or_min != self.maximizing:
                actions.reverse()
        else:
            actions = action_list

        value = -float("inf")
        action_evaluations = dict()
        for action in actions:
            # Get the evaluation of the next action
            next_board_state = self.board_manager.get_successor(action)
            min_val = self.min_value(next_board_state, alpha, beta, depth - 1, start_time)
            self.board_manager.get_predecessor()

            # Check if time has run out
            if min_val is None or timer() - start_time >= self.max_time:
                return None

            # Set the maximum so far
            value = max(value, min_val)

            if value >= beta:
                return value

            alpha = max(value, alpha)
            action_evaluations[action] = value

        # Sort high to low evaluations
        sorted_action_list = [action for action, value in sorted(action_evaluations.items(), key=lambda x: -x[1])]
        self.sorted_action_lists[action_list] = sorted_action_list, self.maximizing

        return value

    def min_value(self, board_state, alpha, beta, depth, start_time):
        if board_state.determine_winner() is not None:
            return self.get_evaluation()
        elif self.find_win(board_state, white_to_move=not self.is_white):
            return -self.winning_value

        # Check if we have seen this list of actions before
        action_list = tuple(board_state.get_action_list())
        if action_list in self.sorted_action_lists:
            actions, max_or_min = self.sorted_action_lists[action_list]
            if max_or_min != self.minimizing:
                actions.reverse()
        else:
            actions = action_list

        value = float("inf")
        action_evaluations = dict()
        for action in actions:
            # Get the evaluation of the next action
            next_board_state = self.board_manager.get_successor(action)
            max_val = self.max_value(next_board_state, alpha, beta, depth - 1, start_time)
            self.board_manager.get_predecessor()

            # Check if time has run out
            if max_val is None or timer() - start_time >= self.max_time:
                return None

            # Set the maximum so far
            value = min(value, max_val)

            if value <= alpha:
                return value

            beta = min(value, beta)
            action_evaluations[action] = value

        # Sort low to high evaluations
        sorted_action_list = [action for action, value in sorted(action_evaluations.items(), key=lambda x: x[1])]
        self.sorted_action_lists[action_list] = sorted_action_list, self.minimizing

        return value

    @staticmethod
    def find_win(current_state, white_to_move=True):
        """
        This function is called when minimax finds a scenario with 5 pieces surrounding the opponent's queen bee.
        This checks if any allied piece can move there immediately during the next turn, this function returns True.

        :return bool: True if a checkmate is possible, False otherwise.
        """
        if current_state.black_queen_location is None or current_state.white_queen_location is None:
            return False
        if white_to_move:
            black_qb = current_state.pieces[current_state.black_queen_location]
            if len(black_qb.connected_pieces) == 5:
                last_empty_space = black_qb.connected_empty_spaces.copy().pop()
                for piece_location, moves in current_state.white_possible_moves.items():
                    if last_empty_space in moves and piece_location not in black_qb.connected_pieces:
                        return True
                if last_empty_space in current_state.white_locations_to_place:
                    return True
        else:
            white_qb = current_state.pieces[current_state.white_queen_location]
            if len(white_qb.connected_pieces) == 5:
                last_empty_space = white_qb.connected_empty_spaces.copy().pop()
                for piece_location, moves in current_state.black_possible_moves.items():
                    if last_empty_space in moves and piece_location not in white_qb.connected_pieces:
                        return True
                if last_empty_space in current_state.black_locations_to_place:
                    return True
        return False


class ExpectimaxAI(MinimaxAI):

    def __init__(self, is_white=True, board_manager=None, max_depth=4, max_time=5):
        super().__init__(is_white, board_manager, max_depth, max_time)
        self.name = f'Expectimax AI with Depth {self.max_depth}'

    def min_value(self, board_state, alpha, beta, current_depth, start_time):
        return self.expected_value(board_state, alpha, beta, current_depth, start_time)

    def expected_value(self, board_state, alpha, beta, current_depth, start_time):
        if current_depth <= 0 or board_state.determine_winner() is not None:
            return self.get_evaluation()

        sum_of_values = 0
        actions = board_state.get_action_list()
        for action in actions:
            next_board_state = self.board_manager.get_successor(action)
            sum_of_values += self.max_value(next_board_state, alpha, beta, current_depth - 1, start_time)
            self.board_manager.get_predecessor()

            if timer() - start_time >= self.max_time:
                break

        return sum_of_values / len(actions)
