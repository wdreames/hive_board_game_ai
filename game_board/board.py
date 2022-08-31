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

            # TODO: [Turns] Would be able to automatically know which player's turn it is with turn_number via odd/even
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

    # TODO: [Turns] Need to allow all empty spaces for placement on turns 1 and 2
    def place_piece(self, player, piece_type, location):
        if player == 'white':
            if self.white_pieces_to_place[piece_type] > 0 and location in self.white_locations_to_place:
                self.white_pieces_to_place[piece_type] -= 1
                if piece_type == 'Ant':
                    Ant(location[0], location[1], is_white=True)
                elif piece_type == 'Queen Bee':
                    QueenBee(location[0], location[1], is_white=True)
                elif piece_type == 'Grasshopper':
                    Grasshopper(location[0], location[1], is_white=True)
            else:
                print('Error: You either do not have any more of this type of piece or cannot place a piece there.')
        elif player == 'black':
            if self.black_pieces_to_place[piece_type] > 0:  # and location in self.black_locations_to_place:
                self.black_pieces_to_place[piece_type] -= 1
                if piece_type == 'Ant':
                    Ant(location[0], location[1], is_white=False)
                elif piece_type == 'Queen Bee':
                    QueenBee(location[0], location[1], is_white=False)
                elif piece_type == 'Grasshopper':
                    Grasshopper(location[0], location[1], is_white=False)
            else:
                print('Error: You either do not have any more of this type of piece or cannot place a piece there.')

    # TODO: [Turns] Remember that the queen bee must be placed <= move 4
    def get_all_possible_actions(self, player):
        pieces_to_play, locations_to_place = self.get_all_possible_placements(player)

        # TODO: [Movement] Add movement actions

        return pieces_to_play, locations_to_place

    def get_all_possible_placements(self, player):
        if player == 'white':
            pieces_to_play = self.white_pieces_to_place
            locations_to_place = self.white_locations_to_place
        else:
            pieces_to_play = self.black_pieces_to_place
            locations_to_place = self.black_locations_to_place

        return pieces_to_play, locations_to_place

    def calc_all_possible_actions(self):
        pass

    def calc_possible_moves(self, player):
        pass

    def perform_action(self):
        pass

    def move_piece(self, player, piece, new_location):
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
