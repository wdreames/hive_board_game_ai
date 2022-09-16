from src.game_board.empty_space import EmptySpace
from src.game_board.piece import Piece
from src.game_board.pieces.ant import Ant
from src.game_board.pieces.grasshopper import Grasshopper
from src.game_board.pieces.queen_bee import QueenBee


class HiveGameBoard(object):
    """
    This class is used to store the board state of the game. A singleton design pattern is used for this class so there
    can only ever be one instance of the game board. This can be accessed across all files.
    """

    MOVE_PIECE = 'move'
    PLACE_PIECE = 'place'

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
                Piece.ANT: 5,
                Piece.QUEEN_BEE: 1,
                Piece.GRASSHOPPER: 5
            }
            cls.black_pieces_to_place = {
                Piece.ANT: 5,
                Piece.QUEEN_BEE: 1,
                Piece.GRASSHOPPER: 5
            }

            cls.turn_number = 1
            cls.white_locations_to_place = set()
            cls.black_locations_to_place = set()
            cls.white_possible_moves = dict()
            cls.black_possible_moves = dict()
            cls.white_queen_location = None
            cls.black_queen_location = None

            # Create board with one empty square
            EmptySpace(0, 0)
            cls.white_locations_to_place = {(0, 0)}

            cls.spaces_requiring_updates = set()

        return cls.instance

    def perform_action(self, action_type, piece_type, piece_location, new_piece_location):
        if action_type == HiveGameBoard.MOVE_PIECE:
            self.move_piece(piece_location, new_piece_location)
        elif action_type == HiveGameBoard.PLACE_PIECE:
            self.place_piece(piece_type, piece_location)
        else:
            raise ValueError('Action type can only be MOVE_PIECE or PLACE_PIECE')

        # TODO: [Organization] Test cases will need to be restructured in order to call the following here
        # End of action bookkeeping
        # for space in self.spaces_requiring_updates:
        #     space.update()
        # self.spaces_requiring_updates.clear()
        #
        # self.turn_number += 1

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

    def get_all_possible_moves(self):
        if self.is_white_turn():
            return self.white_possible_moves
        else:
            return self.black_possible_moves

    def place_piece(self, piece_type, location):
        """
        Place a piece on the game board.

        :param piece_type: string
            String represenation of the type of piece being placed. If there are no more pieces of this type to place,
            the piece will not be placed. These are the options currently implemented:
            - Piece.ANT
            - Piece.GRASSHOPPER
            - Piece.QUEEN_BEE
        :param location: tuple
            Coordinate of the location this piece will be placed. This location must be in the list of possible
            locations for the current player to place a piece or it will not be placed.
        """
        # Gather the valid pieces and locations
        pieces_to_place, locations_to_place = self.get_all_possible_placements()

        # Ensure the move is legal then place the piece
        if pieces_to_place.get(piece_type, 0) > 0 and location in locations_to_place:
            pieces_to_place[piece_type] -= 1
            if piece_type == Piece.ANT:
                Ant(location[0], location[1], is_white=self.is_white_turn())
            elif piece_type == Piece.QUEEN_BEE:
                QueenBee(location[0], location[1], is_white=self.is_white_turn())
                if self.is_white_turn():
                    self.white_pieces_to_place[Piece.QUEEN_BEE] = 0
                else:
                    self.black_pieces_to_place[Piece.QUEEN_BEE] = 0
            elif piece_type == Piece.GRASSHOPPER:
                Grasshopper(location[0], location[1], is_white=self.is_white_turn())
            else:
                raise ValueError(f'{piece_type} is not a valid type of piece.')
        else:
            raise ValueError('You either do not have any more of this type of piece or cannot place a piece there.')

        # End of action bookkeeping
        all_spaces = self.get_all_spaces()
        for space in self.spaces_requiring_updates:
            if space in all_spaces:
                all_spaces[space].update()
        self.spaces_requiring_updates.clear()

        self.turn_number += 1

    def move_piece(self, piece, new_location):
        self.pieces[piece].move_to(new_location)

        # End of action bookkeeping
        all_spaces = self.get_all_spaces()
        for space in self.spaces_requiring_updates:
            if space in all_spaces:
                all_spaces[space].update()
        self.spaces_requiring_updates.clear()

        self.turn_number += 1

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
            return 'draw'
        elif self._black_queen_surrounded():
            return 'white'
        elif self._white_queen_surrounded():
            return 'black'
        else:
            return None

    # TODO: [UI] This is a temporary solution. Do not use this in the final product...
    def print_board(self):
        if not self.pieces:
            return

        piece_coords = list(self.pieces.keys())
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
