import game_board.board as board
import game_board.empty_space as emt

from abc import abstractmethod
from game_board.hex_space import HexSpace


class Piece(HexSpace):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y)
        self.is_white = is_white
        self.possible_moves = set()

        if self.location not in board.HiveGameBoard().empty_spaces:
            print('Error: No empty space at {} to place a piece'.format(self.location))
            # TODO: [UI] throw an actual error
            return

        # Add this piece to the board dictionary
        board.HiveGameBoard().pieces[self.location] = self

        # Copy the empty space at this location's connections
        related_empty_space = board.HiveGameBoard().empty_spaces[self.location]
        self.connected_pieces = related_empty_space.connected_pieces
        self.connected_empty_spaces = related_empty_space.connected_empty_spaces

        # Delete the empty space at this location
        related_empty_space.remove()

        # Increase the count of connected pieces of this color in each empty space
        for point in self.connected_empty_spaces:
            related_empty_space = board.HiveGameBoard().empty_spaces[point]
            if is_white:
                related_empty_space.num_white_connected += 1
            else:
                related_empty_space.num_black_connected += 1
            related_empty_space.update_placement_options()

        # Add new empty spaces
        all_connected_spaces = self.connected_empty_spaces.union(self.connected_pieces)
        surrounding_locations = {(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x - 1, self.y),
                                 (self.x + 1, self.y),
                                 (self.x, self.y + 1), (self.x + 1, self.y + 1)}
        locations_for_new_empty_spaces = surrounding_locations.difference(all_connected_spaces)

        for point in locations_for_new_empty_spaces:
            emt.EmptySpace(point[0], point[1])

    def move(self, new_location):
        pass

    def formed_loop(self):
        # Check if two pieces are on opposite sides after being places
        return False

    @abstractmethod
    def calc_possible_moves(self):
        pass

    def lock(self):
        pass

    def unlock(self):
        pass
