from src.game.spaces import EmptySpace
from src.game.spaces import Piece
from src.game.pieces import Ant
from src.game.pieces import Beetle
from src.game.pieces import Grasshopper
from src.game.pieces import QueenBee
from src.game.pieces import Spider


# TODO: Update Documentation
class HiveGameBoard(object):
    """
    This class is used to store the board state of the game. A singleton design pattern is used for this class so there
    can only ever be one instance of the game board. This can be accessed across all files.
    """

    MOVE_PIECE = 'Move piece'
    PLACE_PIECE = 'Place piece'
    WHITE_WINNER = 'White'
    BLACK_WINNER = 'Black'
    DRAW = 'Draw'

    # TODO: Update Documentation
    # TODO: [AI] Would it be possible to have this return whatever the current instance of the board is?
    #       - This way the AI could traverse down multiple layers, but the internal code would not need to change.
    #       - Question: Would this also be able to manage Piece interactions?
    #         - As long as all actions are called via the board, it should be okay
    #       - Maybe have an instance=board_instance parameter?
    #       - Or I could have a separate BoardManager class that uses Singleton, but can control which board instance
    #       to return when requested.
    def __new__(cls, new_board=False):
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
        if not hasattr(cls, 'instance') or new_board:
            cls.instance = super(HiveGameBoard, cls).__new__(cls)

            cls.pieces = dict()
            cls.empty_spaces = dict()
            cls.white_pieces_to_place = {
                Piece.ANT: 3,
                Piece.BEETLE: 2,
                Piece.GRASSHOPPER: 3,
                Piece.QUEEN_BEE: 1,
                Piece.SPIDER: 2
            }
            cls.black_pieces_to_place = {
                Piece.ANT: 3,
                Piece.BEETLE: 2,
                Piece.GRASSHOPPER: 3,
                Piece.QUEEN_BEE: 1,
                Piece.SPIDER: 2
            }

            cls.turn_number = 1
            cls.white_locations_to_place = set()
            cls.black_locations_to_place = set()
            cls.white_possible_moves = dict()
            cls.black_possible_moves = dict()
            cls.white_queen_location = None
            cls.black_queen_location = None

            cls.spaces_requiring_updates = set()
            cls.empty_spaces_requiring_deletion = set()

            # Variables for keeping track of Ant movement
            cls.ant_mvt_prevention_sets = []
            cls.ant_mvt_preventions_to_add = set()
            cls.ant_locations = set()

            # Variables for determining which pieces can move if a loop was formed
            # cls.loop_was_formed = False
            cls.tarjan_discovery_time = 0
            cls.prepare_to_find_articulation_pts = False

            # Create board with one empty square
            EmptySpace(0, 0)
            cls.white_locations_to_place = {(0, 0)}

        return cls.instance

    # TODO: Documentation
    def perform_action(self, action_type, piece_location, new_location=None, piece_type=None):

        # TODO: [Movement] Will need to ensure Queen Bee is placed <= turn 4. Cannot move if QB not placed
        if action_type == HiveGameBoard.MOVE_PIECE:
            self.move_piece(piece_location, new_location)
        elif action_type == HiveGameBoard.PLACE_PIECE:
            self.place_piece(piece_type, piece_location)
        else:
            raise ValueError('Action type can only be MOVE_PIECE or PLACE_PIECE.')

        # TODO: [Organization] Test cases will need to be restructured in order to call the following here
        # End of action bookkeeping
        # self.update_pieces()
        # self.turn_number += 1

    # TODO: Documentation
    def get_all_possible_actions(self):
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

    # TODO: Documentation
    def get_all_possible_moves(self):
        if self.is_white_turn():
            return self.white_possible_moves
        else:
            return self.black_possible_moves

    # TODO: Documentation
    def add_possible_moves(self, piece_location):
        if self.pieces[piece_location].is_white:
            self.white_possible_moves[piece_location] = self.pieces[piece_location].possible_moves
        else:
            self.black_possible_moves[piece_location] = self.pieces[piece_location].possible_moves

    # TODO: Documentation
    def remove_possible_moves(self, piece_location):
        if piece_location in self.white_possible_moves:
            self.white_possible_moves.pop(piece_location)
        if piece_location in self.black_possible_moves:
            self.black_possible_moves.pop(piece_location)

    # TODO: Update Documentation
    def place_piece(self, piece_type, location):
        """
        Place a piece on the game board.

        :param piece_type: string
            String represenation of the type of piece being placed. If there are no more pieces of this type to place,
            the piece will not be placed. These are the options currently implemented:
            - Piece.ANT
            - Piece.GRASSHOPPER
            - Piece.QUEEN_BEE
            - Piece.BEETLE
            - Piece.SPIDER
        :param location: tuple
            Coordinate of the location this piece will be placed. This location must be in the list of possible
            locations for the current player to place a piece or it will not be placed.
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
            Ant(location[0], location[1], is_white=self.is_white_turn())

        elif piece_type == Piece.BEETLE:
            Beetle(location[0], location[1], is_white=self.is_white_turn())

        elif piece_type == Piece.GRASSHOPPER:
            Grasshopper(location[0], location[1], is_white=self.is_white_turn())

        elif piece_type == Piece.QUEEN_BEE:
            QueenBee(location[0], location[1], is_white=self.is_white_turn())

        elif piece_type == Piece.SPIDER:
            Spider(location[0], location[1], is_white=self.is_white_turn())

        # Reduce piece counts
        if self.is_white_turn():
            self.white_pieces_to_place[piece_type] -= 1
        else:
            self.black_pieces_to_place[piece_type] -= 1

        self.update_pieces()
        self.turn_number += 1

    # TODO: Documentation
    def move_piece(self, piece_location, new_location):
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

        self.update_pieces()
        self.turn_number += 1

    # TODO: Documentation
    def update_pieces(self):
        # TODO: [Efficiency] Add to these sets directly instead of having to use an intersection
        empty_spaces_requiring_updates = self.spaces_requiring_updates.intersection(self.empty_spaces.keys())
        for empty_space_location in empty_spaces_requiring_updates:
            self.empty_spaces[empty_space_location].update()

        self.update_piece_movement()

        pieces_requiring_updates = self.spaces_requiring_updates.intersection(self.pieces.keys())
        for piece_location in pieces_requiring_updates:
            self.pieces[piece_location].update()
        self.spaces_requiring_updates.clear()

    # TODO: Documentation
    def update_piece_movement(self):
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
            # self.white_possible_moves.clear()
            # self.black_possible_moves.clear()
            # for piece_location in non_articulation_points:
            #     self.pieces[piece_location].can_move = True
            #     self.pieces[piece_location].calc_possible_moves()
            for piece_location in articulation_points:
                self.pieces[piece_location].lock()
            for piece_location in non_articulation_points:
                self.pieces[piece_location].unlock()

        self.prepare_to_find_articulation_pts = False

    # TODO: Documentation
    def find_articulation_pts(self, current_coordinate, visited, ap, parent, low, disc_time):
        # Parameters:   current_coordinate: (x,y),
        #               visited: set(coordinates),
        #               articulation_points: set(coordinates),
        #               parent: dict(coordinate: coordinate),
        #               low: int,
        #               disc_time: int
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

    # TODO: Documentation
    def add_to_ant_movement_prevention_set(self, current_space, set_index=None, visited_spaces=None):
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
        if current_space not in self.empty_spaces or current_space not in self.ant_mvt_prevention_sets[set_index]:
            return
        if visited_spaces is None:
            visited_spaces = set()
        self.ant_mvt_prevention_sets[set_index].remove(current_space)
        visited_spaces.add(current_space)

        for connected_space in self.empty_spaces[current_space].get_queen_bee_moves().difference(visited_spaces):
            self.remove_from_ant_movement_prevention_set(connected_space, set_index, visited_spaces)

    # TODO: Documentation
    def union_ant_movement_prevention_sets(self, set_index1, set_index2):
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

    # TODO: Documentation
    def clear_ant_movement_prevention_set(self, set_index):
        self.ant_mvt_prevention_sets.pop(set_index)

    # TODO: Documentation
    # Returns index if it exists
    def empty_space_in_ant_movement_prevention_set(self, space_location):
        for set_index, prevention_set in enumerate(self.ant_mvt_prevention_sets):
            if space_location in prevention_set:
                return set_index
        return -1

    # TODO: Documentation
    def get_all_spaces(self):
        # Merges the dictionaries
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
        return_str += 'white_queen_location: {}\n'.format(self.white_queen_location)
        return_str += 'black_queen_location: {}\n'.format(self.black_queen_location)
        return_str += 'pieces: {}\n'.format(
            [(location, self.pieces[location].name, 'White' if self.pieces[location].is_white else 'Black') for location
             in self.pieces])
        return_str += 'empty_spaces: {}\n'.format(set(self.empty_spaces.keys()))
        return return_str
