import copy

from src.game.spaces import EmptySpace
from src.game.spaces import Piece
from src.game.pieces import Ant
from src.game.pieces import Beetle
from src.game.pieces import Grasshopper
from src.game.pieces import QueenBee
from src.game.pieces import Spider


class BoardManager:

    def __new__(cls, new_manager=False):
        if not hasattr(cls, 'instance') or new_manager:
            cls.instance = super(BoardManager, cls).__new__(cls)
            board = HiveGameBoard()
            cls.root_board = board
            cls.current_board = board
        return cls.instance

    # def __init__(self):
    #     self.root_board = HiveGameBoard()
    #     self.current_board = self.root_board

    def reset_board(self):
        self.set_board(self.root_board)

    def set_board(self, new_board):
        self.current_board = new_board

    def get_board(self):
        return self.current_board

    def get_successor(self, board_instance=None, action=None):
        if action is None:
            return self.get_board()
        if board_instance is None:
            board_instance = self.get_board()
        successor_board = copy.deepcopy(board_instance)
        successor_board.perform_action(action)
        return successor_board

    def get_action_list(self):
        return self.root_board.get_action_list()

    def perform_action(self, action):
        self.root_board.perform_action(action)

    def __str__(self):
        return str(self.current_board)


# TODO: Update Documentation
class HiveGameBoard:
    """
    This class is used to store the board state of the game. A singleton design pattern is used for this class so there
    can only ever be one instance of the game board. This can be accessed across all files.
    """

    MOVE_PIECE = 'Move piece'
    PLACE_PIECE = 'Place piece'
    WHITE_WINNER = 'White'
    BLACK_WINNER = 'Black'
    DRAW = 'Draw'

    # TODO: [AI] Would it be possible to have this return whatever the current instance of the board is?
    #       - This way the AI could traverse down multiple layers, but the internal code would not need to change.
    #       - Question: Would this also be able to manage Piece interactions?
    #         - As long as all actions are called via the board, it should be okay
    #       - Maybe have an instance=board_instance parameter?
    #       - Or I could have a separate BoardManager class that uses Singleton, but can control which board instance
    #       to return when requested.
    def __init__(self):
        """
        Method used to get an instance of the game board. A singleton design pattern is used here so the class is
        only initialized the first time it is called.

        This begins the game with an empty space at (0, 0), with white having the first move.

        :param new_board: boolean
            When this parameter is set to True, the game board is reset. False by default
        """
        # TODO: [NOTE] I'll probably need to trash the singleton design pattern when I start simulating moves...
        # TODO: [NOTE] Although I could create a main class as a singleton and have the same effect
        # Singleton design pattern
        # if not hasattr(cls, 'instance') or new_board:
        #     cls.instance = super(HiveGameBoard, cls).__new__(cls)

        self.pieces = dict()
        self.empty_spaces = dict()
        self.white_pieces_to_place = {
            Piece.ANT: 3,
            Piece.BEETLE: 2,
            Piece.GRASSHOPPER: 3,
            Piece.QUEEN_BEE: 1,
            Piece.SPIDER: 2
        }
        self.black_pieces_to_place = {
            Piece.ANT: 3,
            Piece.BEETLE: 2,
            Piece.GRASSHOPPER: 3,
            Piece.QUEEN_BEE: 1,
            Piece.SPIDER: 2
        }

        self.turn_number = 1
        self.white_locations_to_place = set()
        self.black_locations_to_place = set()
        self.white_possible_moves = dict()
        self.black_possible_moves = dict()
        self.white_queen_location = None
        self.black_queen_location = None

        # Used for evaluating state
        self.num_white_free_pieces = {
            Piece.ANT: 0,
            Piece.BEETLE: 0,
            Piece.GRASSHOPPER: 0,
            Piece.QUEEN_BEE: 0,
            Piece.SPIDER: 0
        }
        self.num_black_free_pieces = {
            Piece.ANT: 0,
            Piece.BEETLE: 0,
            Piece.GRASSHOPPER: 0,
            Piece.QUEEN_BEE: 0,
            Piece.SPIDER: 0
        }

        self.spaces_requiring_updates = set()
        self.empty_spaces_requiring_deletion = set()

        # Variables for keeping track of Ant movement
        self.ant_mvt_prevention_sets = []
        self.ant_mvt_preventions_to_add = set()
        self.ant_locations = set()

        # Variables for determining which pieces can move if a loop was formed
        # self.loop_was_formed = False
        self.tarjan_discovery_time = 0
        self.prepare_to_find_articulation_pts = False

        # Create board with one empty square
        EmptySpace(self, 0, 0)
        self.white_locations_to_place = {(0, 0)}

    def perform_action(self, action):
        action_type = action[0]
        piece_location = action[1]
        action_variable = action[2]

        print(action)

        if action_type == HiveGameBoard.PLACE_PIECE:
            self.perform_action_helper(action_type, piece_location, piece_type=action_variable)
        else:
            self.perform_action_helper(action_type, piece_location, new_location=action_variable)

    def perform_action_helper(self, action_type, piece_location, new_location=None, piece_type=None):
        """
        Performs an action on the game board. Possible actions are HiveGameBoard.MOVE_PIECE or HiveGameBoard.PLACE_PIECE

        :param action_type:
            Must be HiveGameBoard.MOVE_PIECE or HiveGameBoard.PLACE_PIECE
        :param piece_location: (x, y)
            When placing a Piece, this is the location the Piece will be placed.
            When moving a Piece, this is the initial location of the Piece.
        :param new_location: (x, y)
            This parameter is only used when moving a Piece. This is the location the Piece is moving to.
        :param piece_type:
            This parameter is only used when placing a Piece. This specifies the type of Piece being placed.
            Must be Piece.ANT, Piece.BEETLE, Piece.GRASSHOPPER, Piece.QUEEN_BEE, or Piece.SPIDER.
        :raises ValueError:
            A ValueError will be raised if action_types other than HiveGameBoard.MOVE_PIECE or HiveGameBoard.PLACE_PIECE
            are used.
        """

        if action_type == HiveGameBoard.MOVE_PIECE:
            self.move_piece(piece_location, new_location)
        elif action_type == HiveGameBoard.PLACE_PIECE:
            self.place_piece(piece_type, piece_location)
        else:
            raise ValueError('Action type can only be HiveGameBoard.MOVE_PIECE or HiveGameBoard.PLACE_PIECE.')

    def get_action_list(self):
        pieces_to_play, locations_to_place, possible_moves_dict = self.get_all_possible_actions()

        all_actions = []
        # Place actions
        for piece_type, amount_of_type in pieces_to_play.items():
            if amount_of_type:
                for possible_location in locations_to_place:
                    all_actions.append((
                        HiveGameBoard.PLACE_PIECE,
                        possible_location,
                        piece_type
                    ))

        # Move actions
        for piece_location, move_locations in possible_moves_dict.items():
            for new_location in move_locations:
                all_actions.append([
                    HiveGameBoard.MOVE_PIECE,
                    piece_location,
                    new_location
                ])

        return all_actions

    def get_all_possible_actions(self):
        """
        Gathers all possible actions (possible moves for Pieces on the board and locations to place new Pieces)
        for the current player.

        :return: (dict, set, dict)
            The returned tuple contains:
            0. A dictionary of {piece_type: amount_of_that_type}
            1. A set of possible locations to place new pieces
            2. A dictionary of {piece_location: possible_moves_for_that_piece}
        """
        pieces_to_play, locations_to_place = self.get_all_possible_placements()
        possible_moves_dict = self.get_all_possible_moves()
        return pieces_to_play, locations_to_place, possible_moves_dict

    def get_all_possible_placements(self):
        """
        Gathers the pieces the current player can place as well as all the possible placement locations for that player.
        :return: (dict, set)
            tuple containing a dictionary of the remaining pieces to play, and a set containing the coordinates
            at which the player can place pieces.
        """
        if self.is_white_turn():
            # The queen bee must be placed before move 4
            if (self.turn_number + 1) // 2 == 4 and self.white_queen_location is None:
                pieces_to_play = {'Queen Bee': 1}
            else:
                pieces_to_play = self.white_pieces_to_place
            locations_to_place = self.white_locations_to_place
        else:
            # The queen bee must be placed before move 4
            if (self.turn_number + 1) // 2 == 4 and self.black_queen_location is None:
                pieces_to_play = {'Queen Bee': 1}
            else:
                pieces_to_play = self.black_pieces_to_place
            locations_to_place = self.black_locations_to_place

        if self.turn_number == 1 or self.turn_number == 2:
            locations_to_place = self.white_locations_to_place.union(self.black_locations_to_place)

        return pieces_to_play, locations_to_place

    def get_all_possible_moves(self):
        """
        Gathers the set of all possible moves for the current player. This is stored as a dictionary where Piece
        locations are keys and their set of possible moves are the values.

        :return: dict {piece_location: possible_moves_for_that_piece}
        """
        if self.is_white_turn():
            if self.white_queen_location is None:
                return dict()
            return self.white_possible_moves
        else:
            if self.black_queen_location is None:
                return dict()
            return self.black_possible_moves

    def add_possible_moves(self, piece_location):
        """
        Gathers an updated set of moves for the Piece at the specified location.

        :param piece_location: (x, y)
            Location of the Piece which has new moves to add to the game board.
        """
        if self.pieces[piece_location].is_white:
            self.white_possible_moves[piece_location] = self.pieces[piece_location].possible_moves
        else:
            self.black_possible_moves[piece_location] = self.pieces[piece_location].possible_moves

    def remove_possible_moves(self, piece_location):
        """
        Removes all moves recorded in the game board for the Piece at the specified location.

        :param piece_location: (x, y)
            Location of the Piece which will no longer have any moves on game board.
        """
        if piece_location in self.white_possible_moves:
            self.white_possible_moves.pop(piece_location)
        if piece_location in self.black_possible_moves:
            self.black_possible_moves.pop(piece_location)

    def place_piece(self, piece_type, location):
        """
        Place a Piece on the game board.

        :param piece_type:
            The following are the options for the types of Pieces that can be placed:
            - Piece.ANT
            - Piece.GRASSHOPPER
            - Piece.QUEEN_BEE
            - Piece.BEETLE
            - Piece.SPIDER
        :param location: (x, y)
            Location where this piece will be placed. This location must be in the list of possible
            locations for the current player to place a piece.
        :raises RuntimeError:
            A RuntimeError will be raised in the following cases:
            - The current player is placing a Piece other than a Queen Bee on their fourth turn and a Queen Bee has not
              been placed prior to this turn. The Queen Bee must be placed before or on the player's fourth turn.
            - An invalid Piece type is entered.
            - The player does not have any more of the specified type of Piece in their reserve.
            - The player cannot place a Piece at the specified location.
        """
        # Gather the valid pieces and locations
        pieces_to_place, locations_to_place = self.get_all_possible_placements()

        # Ensure action validity
        player = 'White' if self.is_white_turn() else 'Black'
        NO_QUEEN_BEE_PLACED_ERR = 'Illegal action. You must place your Queen Bee by your fourth turn.'
        INVALID_PIECE_ERR = f'Illegal action. {piece_type} is not a valid type of piece.'
        NO_PIECE_ERR = f'Illegal action. {player} does not have any more {piece_type}s to place.'
        INVALID_LOCATION_ERR = f'Illegal action. {player} cannot place a piece at {location}.'
        if piece_type not in pieces_to_place:
            if pieces_to_place == {Piece.QUEEN_BEE: 1}:
                raise RuntimeError(NO_QUEEN_BEE_PLACED_ERR)
            else:
                raise RuntimeError(INVALID_PIECE_ERR)
        if pieces_to_place[piece_type] <= 0:
            raise RuntimeError(NO_PIECE_ERR)
        if location not in locations_to_place:
            raise RuntimeError(INVALID_LOCATION_ERR)

        # Place the piece
        if piece_type == Piece.ANT:
            Ant(self, location[0], location[1], is_white=self.is_white_turn())
        elif piece_type == Piece.BEETLE:
            Beetle(self, location[0], location[1], is_white=self.is_white_turn())
        elif piece_type == Piece.GRASSHOPPER:
            Grasshopper(self, location[0], location[1], is_white=self.is_white_turn())
        elif piece_type == Piece.QUEEN_BEE:
            QueenBee(self, location[0], location[1], is_white=self.is_white_turn())
        elif piece_type == Piece.SPIDER:
            Spider(self, location[0], location[1], is_white=self.is_white_turn())

        # Reduce piece counts
        if self.is_white_turn():
            self.white_pieces_to_place[piece_type] -= 1
        else:
            self.black_pieces_to_place[piece_type] -= 1

        self.update_spaces()
        self.turn_number += 1

    def move_piece(self, piece_location, new_location):
        """
        Move a Piece on the game board.

        :param piece_location: (x, y)
            Initial location of the Piece
        :param new_location: (x, y)
            New location for the Piece.
        :raises RuntimeError:
            A RuntimeError will be raised in the following cases:
            - The current player has not placed a Queen Bee before making a move action.
            - The current player attempts to make a move for a Piece they do not control.
            - The specified Piece cannot move based on the "One Hive" rule.
            - The new location is not within the Piece's list of possible moves.
        """
        if piece_location == new_location:
            return

        # Ensure the move is legal
        NO_QUEEN_BEE_MOVE_ERR = 'Illegal action. You must place your Queen Bee before you can perform a move action.'
        WHITE_MOVE_ERR = "Illegal action. It is white's turn, but a move for black was attempted."
        BLACK_MOVE_ERR = "Illegal action. It is black's turn, but a move for white was attempted."
        ONE_HIVE_ERR = 'Illegal action. This piece cannot move based on the "One Hive" rule.'
        INVALID_MOVE_ERR = 'Illegal action. This piece cannot move to the specified location.'
        if self.is_white_turn():
            if self.white_queen_location is None:
                raise RuntimeError(NO_QUEEN_BEE_MOVE_ERR)
            elif not self.pieces[piece_location].is_white:
                raise RuntimeError(WHITE_MOVE_ERR)
            elif piece_location not in self.white_possible_moves:
                raise RuntimeError(ONE_HIVE_ERR)
            elif new_location not in self.white_possible_moves[piece_location]:
                raise RuntimeError(INVALID_MOVE_ERR)
        else:
            if self.black_queen_location is None:
                raise RuntimeError(NO_QUEEN_BEE_MOVE_ERR)
            elif self.pieces[piece_location].is_white:
                raise RuntimeError(BLACK_MOVE_ERR)
            elif piece_location not in self.black_possible_moves:
                raise RuntimeError(ONE_HIVE_ERR)
            elif new_location not in self.black_possible_moves[piece_location]:
                raise RuntimeError(INVALID_MOVE_ERR)

        self.pieces[piece_location].move_to(new_location)

        self.update_spaces()
        self.turn_number += 1

    def update_spaces(self):
        """
        Updates all spaces on the game board requiring an update. This should only be called at the end of a turn.
        """
        # TODO: [Efficiency] Add to these sets directly instead of having to use an intersection
        empty_spaces_requiring_updates = self.spaces_requiring_updates.intersection(self.empty_spaces.keys())
        for empty_space_location in empty_spaces_requiring_updates:
            self.empty_spaces[empty_space_location].update()

        self.update_piece_movement()

        pieces_requiring_updates = self.spaces_requiring_updates.intersection(self.pieces.keys())
        for piece_location in pieces_requiring_updates:
            self.pieces[piece_location].update()
        self.spaces_requiring_updates.clear()

    def update_piece_movement(self):
        """
        Updates the movement for certain Pieces. This involves updating Ant movement prevention sets, along with
        updating movement rules for all Pieces based on the "One Hive" rule.
        """
        # Ant movement specific
        for location in self.ant_mvt_preventions_to_add:
            self.add_to_ant_movement_prevention_set(location)
        self.ant_mvt_preventions_to_add.clear()

        # Determine which pieces can move under the OneHive rule
        if self.turn_number <= 2:
            [piece.unlock() for piece in self.pieces.values()]
        elif self.prepare_to_find_articulation_pts:
            # TODO: [Efficiency] See if there is a faster way to find a starting coordinate
            start_coordinate = set(self.pieces.keys()).pop()
            visited_pieces = set()
            articulation_points = set()
            parent_nodes = dict()
            low_values = dict()
            discovery_times = dict()
            self.find_articulation_pts(start_coordinate, visited_pieces, articulation_points,
                                       parent_nodes, low_values, discovery_times)

            # TODO: [Efficiency] I feel like there may be an easier/faster way to do this
            non_articulation_points = set(self.pieces.keys()).difference(articulation_points)
            for piece_location in articulation_points:
                self.pieces[piece_location].lock()
            for piece_location in non_articulation_points:
                self.pieces[piece_location].unlock()

        self.prepare_to_find_articulation_pts = False

    def find_articulation_pts(self, current_coordinate, visited, ap, parent, low, disc_time):
        """
        This is used to determine which Pieces can move under the "One Hive" rule. It finds all Pieces that are
        articulation points, or points within a graph that cannot be removed without splitting the graph. This
        function implements Tarjan's algorithm.

        :param current_coordinate: (x, y)
            Location of the current Piece being checked.
        :param visited: set {(x1, y1), (x2, y2)}
            Set of locations the algorithm has already seen.
        :param ap: set {(x1, y1), (x2, y2)}
            Set of all articulation points.
        :param parent: dict {(x, y): (parent_x, parent_y)}
            Dictionary relating a location to its parent location within the graph traversal tree.
        :param low: dict {(x, y): low_value}
            Dictionary relating a location to the minimum discovery step. Indicated the topmost reachable ancestor
            within the traversal.
        :param disc_time: dict {(x, y): discovery_time}
            Dictionary relating a location to the step in the traversal that it was discovered.
        :return:
        """
        children = 0
        visited.add(current_coordinate)
        disc_time[current_coordinate] = self.tarjan_discovery_time
        low[current_coordinate] = self.tarjan_discovery_time
        self.tarjan_discovery_time += 1

        for connected_location in self.pieces[current_coordinate].connected_pieces:
            if connected_location not in visited:
                parent[connected_location] = current_coordinate
                children += 1

                self.find_articulation_pts(connected_location, visited, ap, parent, low, disc_time)

                low[current_coordinate] = min(low[connected_location], low[current_coordinate])

                if current_coordinate not in parent and children > 1:
                    ap.add(current_coordinate)
                elif current_coordinate in parent and low[connected_location] >= disc_time[current_coordinate]:
                    ap.add(current_coordinate)
            elif parent.get(current_coordinate) and connected_location != parent.get(current_coordinate):
                low[current_coordinate] = min(low[current_coordinate], disc_time[connected_location])

    def add_to_ant_movement_prevention_set(self, current_space, set_index=None, visited_spaces=None):
        """
        Adds EmptySpaces to an Ant movement prevention set. This starts at an initial location, then uses a
        depth-first search algorithm to add any other empty spaces the given location can slide into.

        :param current_space: (x, y)
            The location to add to the set.
        :param set_index: int
            The index of the prevention set within self.ant_mvt_prevention_sets. If None is entered for the set index,
            a new set is added to the list of prevention sets.
            Default is None.
        :param visited_spaces: set
            Set of spaces the algorithm has seen already.
            Default is an empty set.
        """
        if current_space not in self.empty_spaces:
            return
        if visited_spaces is None:
            visited_spaces = set()
        if set_index is None:
            self.ant_mvt_prevention_sets.append(set())
            set_index = -1

        # If the edge of the board is ever reached, this should no longer be a set
        if self.empty_spaces[current_space].get_total_num_connections() < 6:
            self.ant_mvt_prevention_sets[set_index].clear()
            return

        self.ant_mvt_prevention_sets[set_index].add(current_space)
        visited_spaces.add(current_space)

        for connected_space in self.empty_spaces[current_space].get_queen_bee_moves().difference(visited_spaces):
            self.add_to_ant_movement_prevention_set(connected_space, set_index, visited_spaces)

    # TODO: Documentation
    def remove_from_ant_movement_prevention_set(self, current_space, set_index, visited_spaces=None):
        """
        Removes EmptySpaces from an Ant movement prevention set. This starts at an initial location, then uses a
        depth-first search algorithm to remove any other empty spaces the given location can slide into.

        :param current_space: (x, y)
            The location to remove from the set.
        :param set_index: int
            The index of the prevention set within self.ant_mvt_prevention_sets.
        :param visited_spaces: set
            Set of spaces the algorithm has seen already.
            Default is an empty set.
        """
        if current_space not in self.empty_spaces or current_space not in self.ant_mvt_prevention_sets[set_index]:
            return
        if visited_spaces is None:
            visited_spaces = set()
        self.ant_mvt_prevention_sets[set_index].remove(current_space)
        visited_spaces.add(current_space)

        for connected_space in self.empty_spaces[current_space].get_queen_bee_moves().difference(visited_spaces):
            self.remove_from_ant_movement_prevention_set(connected_space, set_index, visited_spaces)

    def union_ant_movement_prevention_sets(self, set_index1, set_index2):
        """
        Combines to Ant movement prevention sets into one set.

        :param set_index1: int
            Index of the first set within self.ant_mvt_prevention_sets
        :param set_index2: int
            Index of the second set within self.ant_mvt_prevention_sets
        :return: int
            Index of the resulting set.
        """
        if set_index1 == set_index2:
            return set_index1

        # We want to make sure we are removing the larger index so that the index left in the list is not changed.
        if set_index1 < set_index2:
            i1 = set_index1
            i2 = set_index2
        else:
            i1 = set_index2
            i2 = set_index1

        self.ant_mvt_prevention_sets[i1] = self.ant_mvt_prevention_sets[i1].union(
            self.ant_mvt_prevention_sets[i2]
        )
        self.clear_ant_movement_prevention_set(i2)
        return i1

    def clear_ant_movement_prevention_set(self, set_index):
        """
        Removes an Ant movement prevention set from self.ant_mvt_prevention_sets

        :param set_index: int
            Index of the set to remove from the list
        """
        del self.ant_mvt_prevention_sets[set_index]

    def empty_space_in_ant_movement_prevention_set(self, space_location):
        """
        Check if an EmptySpace exists within an Ant movement prevention set. If it does, this function returns the
        index of that set. If it does not, the function will return -1.

        :param space_location: (x, y)
            Location of the EmptySpace to find in an Ant movement prevention set.
        :return: int
            Index of the set the EmptySpace resides in. If the EmptySpace could not be found in any Ant movement
            prevention set, -1 is returned instead.
        """
        for set_index, prevention_set in enumerate(self.ant_mvt_prevention_sets):
            if space_location in prevention_set:
                return set_index
        return -1

    def get_all_spaces(self):
        """
        Gathers all spaces (Pieces and EmptySpaces) on the game board

        :return: dict {(x, y): HexSpace}
            Dictionary relating a location to the HexSpace object at that location.
        """
        # Pieces will overwrite empty spaces at the same location
        return {**self.empty_spaces, **self.pieces}

    def _black_queen_surrounded(self):
        """
        Determines if the black queen is surrounded (white has met the win condition)
        :return: bool
        """
        if self.black_queen_location is not None:
            return len(self.pieces[self.black_queen_location].connected_pieces) == 6
        else:
            return False

    def _white_queen_surrounded(self):
        """
        Determines if the white queen is surrounded (black has met the win condition)
        :return: bool
        """
        if self.white_queen_location is not None:
            return len(self.pieces[self.white_queen_location].connected_pieces) == 6
        else:
            return False

    def is_white_turn(self):
        """
        Used to determine if it is white or black's turn
        :return: bool
            True if it is white's turn; False if it is black's turn
        """
        return self.turn_number % 2 == 1

    def determine_winner(self):
        """
        Determines if either player has won the game. Also determines if a draw has been made
        :return: string or None
            Returns None if neither player has won yet
            Returns 'white' if White has won
            Returns 'black' if Black has won
            Returns 'draw' if the game is a draw
        """
        if self._black_queen_surrounded() and self._white_queen_surrounded():
            return HiveGameBoard.DRAW
        elif self._black_queen_surrounded():
            return HiveGameBoard.WHITE_WINNER
        elif self._white_queen_surrounded():
            return HiveGameBoard.BLACK_WINNER
        else:
            return None

    # TODO: Documentation
    def evaluate_state(self):
        # Utitlity function:
        # 6 around enemy QB: +10000
        # 5 around enemy QB: +10
        # enemy QB can move: -10
        # Free Ant: +3
        # Free Beetle: +2
        # Free Grasshopper: +2
        # Free Spider: +2
        # Enemy Free Ant: -3
        # Enemy Free Beetle: -2
        # Enemy Free Spider: -2
        # Enemy Free Spider: -2

        if self.is_white_turn():
            num_around_enemy_qb = len(self.pieces[self.black_queen_location].connected_pieces)
            enemy_qb_can_move = 1 if self.black_queen_location in self.black_possible_moves else 0

            player_free_pieces = self.num_white_free_pieces
            enemy_free_pieces = self.num_black_free_pieces
        else:
            num_around_enemy_qb = len(self.pieces[self.white_queen_location].connected_pieces)
            enemy_qb_can_move = 1 if self.white_queen_location in self.black_possible_moves else 0

            player_free_pieces = self.num_black_free_pieces
            enemy_free_pieces = self.num_white_free_pieces

        utilities = [
            1 if num_around_enemy_qb == 6 else 0,
            1 if num_around_enemy_qb == 5 else 0,
            enemy_qb_can_move,

            player_free_pieces[Piece.ANT],
            player_free_pieces[Piece.BEETLE],
            player_free_pieces[Piece.GRASSHOPPER],
            player_free_pieces[Piece.SPIDER],

            enemy_free_pieces[Piece.ANT],
            enemy_free_pieces[Piece.BEETLE],
            enemy_free_pieces[Piece.GRASSHOPPER],
            enemy_free_pieces[Piece.SPIDER],
        ]
        values = [
            10000,
            10,
            -10,
            3,
            2,
            2,
            2,
            -3,
            -2,
            -2,
            -2
        ]

        evaluation = sum([utility * value for utility, value in zip(utilities, values)])
        return evaluation

    # TODO: [UI] This is a temporary solution. Do not use this in the final product...
    def print_board(self):
        if not self.pieces:
            return

        piece_coords = list(self.get_all_spaces().keys())
        piece_coords.sort(key=lambda x: x[0])
        min_x = piece_coords[0][0]
        max_x = piece_coords[-1][0]
        piece_coords.sort(key=lambda y: y[1])
        min_y = piece_coords[0][1]
        max_y = piece_coords[-1][1]

        board_str = ''
        for y in range(0, max_y - min_y + 1):
            for x in range(0, max_x - min_x + 1):
                # Actual points are (x + min_x, y + min_y)
                if (x + min_x, y + min_y) in self.pieces:
                    current_piece = self.pieces[(x + min_x, y + min_y)]
                    piece_char = current_piece.name[:1]
                    if not current_piece.is_white:
                        piece_char = '(' + piece_char + ')'
                    else:
                        piece_char = ' ' + piece_char + ' '
                elif (x + min_x, y + min_y) in self.empty_spaces:
                    piece_char = ' _ '
                else:
                    piece_char = '   '
                if (x + min_x, y + min_y) == (0, 0):
                    board_str += '*{}*|'.format(piece_char)
                else:
                    board_str += ' {} |'.format(piece_char)
            board_str += '\n'
        print(board_str)

    def __str__(self):
        # Used to print the board state
        return_str = ''
        return_str += 'white_pieces_to_place: {}\n'.format(self.white_pieces_to_place)
        return_str += 'black_pieces_to_place: {}\n'.format(self.black_pieces_to_place)
        return_str += 'white_locations_to_place: {}\n'.format(self.white_locations_to_place)
        return_str += 'black_locations_to_place: {}\n'.format(self.black_locations_to_place)
        return_str += 'white_possible_moves: {}\n'.format(self.white_possible_moves)
        return_str += 'black_possible_moves: {}\n'.format(self.black_possible_moves)
        return_str += f'num_white_free_pieces: {self.num_white_free_pieces}\n'
        return_str += f'num_black_free_pieces: {self.num_black_free_pieces}\n'
        return_str += 'white_queen_location: {}\n'.format(self.white_queen_location)
        return_str += 'black_queen_location: {}\n'.format(self.black_queen_location)
        return_str += 'pieces: {}\n'.format(
            [(location, self.pieces[location].name, 'White' if self.pieces[location].is_white else 'Black') for location
             in self.pieces])
        return_str += 'empty_spaces: {}\n'.format(set(self.empty_spaces.keys()))
        return return_str
