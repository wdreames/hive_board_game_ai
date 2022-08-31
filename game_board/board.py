from game_board.empty_space import EmptySpace
from game_board.pieces.ant import Ant
from game_board.pieces.grasshopper import Grasshopper
from game_board.pieces.queen_bee import QueenBee


class HiveGameBoard(object):

    def __new__(cls):

        # TODO: [NOTE] I'll probably need to trash the singleton design pattern when I start simulating moves...
        # TODO: [NOTE] Although I could create a main class as a singleton and have the same effect
        # Singleton design pattern
        if not hasattr(cls, 'instance'):
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

    # TODO: [Turns] Implement and add `self.turn_number += 1`; remove `self.turn_number += 1` from other methods
    def perform_action(self):
        pass

    def place_piece(self, piece_type, location):
        # Gather the valid pieces and locations for each player
        if self.is_white_turn():
            locations_to_place = self.white_locations_to_place
            pieces_to_place = self.white_pieces_to_place
        else:
            locations_to_place = self.black_locations_to_place
            pieces_to_place = self.black_pieces_to_place

        # All open spots are available on moves 1 and 2 for both players
        if self.turn_number == 1 or self.turn_number == 2:
            locations_to_place = self.white_locations_to_place.union(self.black_locations_to_place)

        # Ensure the move is legal then place the piece
        if pieces_to_place[piece_type] > 0 and location in locations_to_place:
            pieces_to_place[piece_type] -= 1
            if piece_type == 'Ant':
                Ant(location[0], location[1], is_white=self.is_white_turn())
            elif piece_type == 'Queen Bee':
                QueenBee(location[0], location[1], is_white=self.is_white_turn())
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
        if self.black_queen_location is not None:
            return len(self.pieces[self.black_queen_location].connected_pieces) == 6
        else:
            return False

    def _white_queen_surrounded(self):
        if self.white_queen_location is not None:
            return len(self.pieces[self.white_queen_location].connected_pieces) == 6
        else:
            return False

    def is_white_turn(self):
        return self.turn_number % 2 == 1

    def determine_winner(self):
        if self._black_queen_surrounded() and self._white_queen_surrounded():
            return 'draw'
        elif self._black_queen_surrounded():
            return 'white'
        elif self._white_queen_surrounded():
            return 'black'
        else:
            return None

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
