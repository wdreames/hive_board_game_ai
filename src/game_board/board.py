from src.game_board.empty_space import EmptySpace
from src.game_board.pieces.ant import Ant
from src.game_board.pieces.grasshopper import Grasshopper
from src.game_board.pieces.queen_bee import QueenBee


class HiveGameBoard(object):
    """
    This class is used to store the board state of the game. A singleton design pattern is used for this class so there
    can only ever be one instance of the game board. This can be accessed across all files.
    """

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
                'Ant': 5,
                'Queen Bee': 1,
                'Grasshopper': 5
            }
            cls.black_pieces_to_place = {
                'Ant': 5,
                'Queen Bee': 1,
                'Grasshopper': 5
            }

            cls.turn_number = 1
            cls.white_locations_to_place = set()
            cls.black_locations_to_place = set()
            cls.white_possible_moves = set()
            cls.black_possible_moves = set()
            cls.white_queen_location = None
            cls.black_queen_location = None

            # Create board with one empty square
            EmptySpace(0, 0)
            cls.white_locations_to_place = {(0, 0)}

        return cls.instance

    def get_all_spaces(self):
        return self.empty_spaces | self.pieces

    # TODO: [Turns] Implement and add `self.turn_number += 1`; remove `self.turn_number += 1` from other methods
    def perform_action(self):
        pass

    def place_piece(self, piece_type, location):
        """
        Place a piece on the game board.

        :param piece_type: string
            String represenation of the type of piece being placed. If there are no more pieces of this type to place,
            the piece will not be placed. These are the options currently implemented:
            - 'Ant'
            - 'Grasshopper'
            - 'Queen Bee'
        :param location: tuple
            Coordinate of the location this piece will be placed. This location must be in the list of possible
            locations for the current player to place a piece or it will not be placed.
        """
        # Gather the valid pieces and locations
        pieces_to_place, locations_to_place = self.get_all_possible_placements()

        # Ensure the move is legal then place the piece
        if pieces_to_place.get(piece_type, 0) > 0 and location in locations_to_place:
            pieces_to_place[piece_type] -= 1
            if piece_type == 'Ant':
                Ant(location[0], location[1], is_white=self.is_white_turn())
            elif piece_type == 'Queen Bee':
                QueenBee(location[0], location[1], is_white=self.is_white_turn())
                if self.is_white_turn():
                    self.white_pieces_to_place['Queen Bee'] = 0
                else:
                    self.black_pieces_to_place['Queen Bee'] = 0
            elif piece_type == 'Grasshopper':
                Grasshopper(location[0], location[1], is_white=self.is_white_turn())
        else:
            print('Error: You either do not have any more of this type of piece or cannot place a piece there.')
            return

        self.turn_number += 1

    def move_piece(self, piece, new_location):
        pass

    def get_all_possible_actions(self):
        pieces_to_play, locations_to_place = self.get_all_possible_placements()

        # TODO: [Movement] Add movement actions
        # TODO: [Turns] Remember that the queen bee must be placed <= move 4

        return pieces_to_play, locations_to_place

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

    def calc_possible_moves(self):
        pass

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
                    piece_char = str(type(current_piece)).split('.')[-1][:1]
                    if not current_piece.is_white:
                        piece_char = '(' + piece_char + ')'
                    else:
                        piece_char = ' ' + piece_char + ' '
                else:
                    piece_char = '   '
                board_str += '{} | '.format(piece_char)
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
        return_str += 'pieces: {}\n'.format(self.pieces)
        return_str += 'empty_spaces: {}\n'.format(self.empty_spaces)
        return return_str
