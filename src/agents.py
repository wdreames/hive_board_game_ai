from abc import abstractmethod
from timeit import default_timer as timer
import src.game.board as board
import src.game.spaces as spaces
import random


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

    @abstractmethod
    def get_action_selection(self):
        pass

    def __str__(self):
        return f'{self.name} ({"White" if self.is_white else "Black"})'


class Player(Agent):

    def __init__(self, is_white=True, board_manager=None):
        super().__init__(is_white, board_manager)
        self.name = 'Player'

    def get_action_selection(self):
        actions = self.board_manager.get_action_list()

        if len(actions) == 1 and actions[0][0] == board.HiveGameBoard.SKIP_TURN:
            print('You have no legal moves. Skipping turn...')
            return actions[0]

        # print(f'The following actions can be played:')
        # for i, action in enumerate(actions):
        #     print(f'{i + 1}: {action}')
        #
        # selection = input('Select an action:')
        # if not selection.isnumeric() or int(selection) not in range(1, len(actions) + 1):
        #     print('Invalid selection. You must enter an integer value from the list of available actions.')
        #     return self.get_action_selection()
        #
        # selected_action = actions[int(selection) - 1]
        # # return selected_action

        return self.make_choice(
            'The following actions can be played:',
            'Select an action:',
            actions
        )

    def make_choice(self, description, prompt, choices):
        print(description)
        for i, choice in enumerate(choices):
            print(f'{i + 1}: {choice}')

        selection = input(prompt)
        if not selection.isnumeric() or int(selection) not in range(1, len(choices) + 1):
            return self.make_choice(description, prompt, choices)

        return choices[int(selection) - 1]


class HexPlayer(Player):

    def __init__(self, is_white=True, board_manager=None):
        super().__init__(is_white, board_manager)
        self.name = 'Player'

    def get_action_selection(self):
        pieces_to_play, locations_to_place, possible_moves_dict = self.board_manager.get_board().get_all_possible_actions()
        ui_id_to_coords = self.board_manager.get_board().ui_id_to_coords
        ui_coords_to_id = self.board_manager.get_board().ui_coords_to_id

        # Check if there are no possible actions
        if not (pieces_to_play and locations_to_place) and not possible_moves_dict:
            print('You have no legal moves. Skipping turn...')
            chosen_action = (board.HiveGameBoard.SKIP_TURN, None, None)

        # Tell the player which pieces they can place
        print('You have the following pieces in your reserve:')
        for piece_type, amount in pieces_to_play.items():
            print(f'\t* {piece_type} x {amount}')

        # Tell the player which pieces they can move

        # Determine if the player is placing or moving a piece
        action_type = self.make_choice(
            'Do you want to place a piece or move a piece?',
            'Select an action type:',
            [board.HiveGameBoard.PLACE_PIECE, board.HiveGameBoard.MOVE_PIECE]
        )

        if action_type == board.HiveGameBoard.PLACE_PIECE:
            pieces_to_play, locations_to_place = self.board_manager.get_board().get_all_possible_placements()
            piece_options = []
            for type_of_piece, amount in pieces_to_play.items():
                if amount:
                    piece_options.append(type_of_piece)
            piece_type = self.make_choice(
                'Which type of piece would you like to place?',
                'Select a type of piece:',
                piece_options
            )

            location_number = self.make_choice(
                f'Where would you like to place a new {piece_type}?',
                'Select a location:',
                [ui_coords_to_id[coordinate] for coordinate in locations_to_place]
            )
            chosen_action = (action_type, ui_id_to_coords[location_number], piece_type)
        else:
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
            evaluation = self.board_manager.get_successor(action).evaluate_state()
            self.board_manager.get_predecessor()
            if not self.is_white:
                evaluation *= -1

            # print(f'{self} - {str(action):45} {evaluation:.2f}')

            if evaluation >= self.winning_value:
                return action
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_actions.clear()
            if evaluation >= best_evaluation:
                best_actions.append(action)

        rand_index = random.randint(0, len(best_actions) - 1)
        return best_actions[rand_index]


class MinimaxAI(Agent):

    def __init__(self, is_white=True, board_manager=None, max_depth=4, max_time=float("inf"), winning_value=10000):
        super().__init__(is_white, board_manager)
        self.max_depth = max_depth if max_depth >= 1 else 1
        self.max_time = max_time if max_time > 0 else 1
        self.name = f'Minimax AI with Depth {self.max_depth}'
        self.winning_value = winning_value

    def get_action_selection(self):
        actions = self.board_manager.get_action_list(randomize_actions=True)

        if len(actions) == 1:
            return actions.pop()

        # Don't think too much during the first few moves
        if (self.board_manager.get_board().turn_number + 1) // 2 < 3:
            random_action = actions.pop()
            while random_action[2] == spaces.Piece.QUEEN_BEE and actions:
                random_action = actions.pop()
            return random_action

        action_evaluations = dict()

        print(f'Number of actions to process: {len(actions)}')
        start_time = timer()
        for d in range(self.max_depth):
            alpha = -self.winning_value
            beta = self.winning_value

            for i, action in enumerate(actions):
                next_board_state = self.board_manager.get_successor(action)
                action_eval = self.min_value(next_board_state, alpha, beta, (d * 2) + 1, start_time)
                self.board_manager.get_predecessor()

                # print(f'{self} - {d + 1} - {str(action):45} {action_eval:.2f} \talpha: {alpha:.2f}')

                if action_eval >= self.winning_value:
                    return action

                action_evaluations[action] = action_eval
                alpha = max(alpha, action_eval)

                if timer() - start_time >= self.max_time:
                    print(f'{self.name} - Depth reached: {d}')
                    # Return the best action that was found
                    return max(action_evaluations.items(), key=lambda x: x[1])[0]

            # If every action is a losing move, return a random action.
            best_action_so_far = max(action_evaluations.items(), key=lambda x: x[1])[0]
            if action_evaluations[best_action_so_far] <= -self.winning_value:
                return best_action_so_far

        print(f'{self.name} - Depth reached: {self.max_depth}')
        # Return the best action that was found
        return max(action_evaluations.items(), key=lambda x: x[1])[0]

    def max_value(self, board_state, alpha, beta, depth, start_time):
        if depth <= 0 or board_state.determine_winner() is not None:
            if self.is_white:
                return board_state.evaluate_state()
            else:
                return -board_state.evaluate_state()

        value = -float("inf")
        actions = board_state.get_action_list(randomize_actions=True)
        # random.shuffle(actions)
        for action in actions:
            next_board_state = self.board_manager.get_successor(action)
            value = max(value, self.min_value(next_board_state, alpha, beta, depth - 1, start_time))
            self.board_manager.get_predecessor()

            if value >= beta or timer() - start_time >= self.max_time:
                return value
            alpha = max(value, alpha)

        return value

    def min_value(self, board_state, alpha, beta, depth, start_time):
        if depth <= 0 or board_state.determine_winner() is not None:
            if self.is_white:
                return board_state.evaluate_state()
            else:
                return -board_state.evaluate_state()

        value = float("inf")
        actions = board_state.get_action_list(randomize_actions=True)
        for action in actions:
            next_board_state = self.board_manager.get_successor(action)
            value = min(value, self.max_value(next_board_state, alpha, beta, depth - 1, start_time))
            self.board_manager.get_predecessor()

            if value <= alpha or timer() - start_time >= self.max_time:
                return value
            beta = min(value, beta)

        return value


class ExpectimaxAI(MinimaxAI):

    def __init__(self, is_white=True, board_manager=None, max_depth=4, max_time=5):
        super().__init__(is_white, board_manager, max_depth, max_time)
        self.name = f'Expectimax AI with Depth {self.max_depth}'

    def min_value(self, board_state, alpha, beta, current_depth, start_time):
        return self.expected_value(board_state, alpha, beta, current_depth, start_time)

    def expected_value(self, board_state, alpha, beta, current_depth, start_time):
        if current_depth <= 0 or board_state.determine_winner() is not None:
            if self.is_white:
                return board_state.evaluate_state()
            else:
                return -board_state.evaluate_state()

        sum_of_values = 0
        actions = board_state.get_action_list()
        for action in actions:
            next_board_state = self.board_manager.get_successor(action)
            sum_of_values += self.max_value(next_board_state, alpha, beta, current_depth - 1, start_time)
            self.board_manager.get_predecessor()

            if timer() - start_time >= self.max_time:
                break

        return sum_of_values / len(actions)
