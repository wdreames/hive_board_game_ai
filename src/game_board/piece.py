import src.game_board.board as board
import src.game_board.empty_space as emt

from abc import abstractmethod
from src.game_board.hex_space import HexSpace


class Piece(HexSpace):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y)
        self.is_white = is_white
        self.possible_moves = set()

        # TODO: [Efficiency] There are some redundant actions here to reduce the amount of written code
        board.HiveGameBoard().pieces[self.location] = self
        self.move_to(self.location)

    def move_to(self, new_location):
        if new_location not in board.HiveGameBoard().empty_spaces:
            print('Error: No empty space at {} to place a piece'.format(new_location))
            # TODO: [UI] Raise an actual error
            return

        # TODO: [Movement] Unlock & disconnect from any relevant pieces that used to be connected

        # Move this piece in the board dictionary
        board.HiveGameBoard().pieces.pop(self.location)
        old_location = self.location
        self.location = new_location
        board.HiveGameBoard().pieces[new_location] = self

        # Update all the connections
        related_empty_space = board.HiveGameBoard().empty_spaces[new_location]
        self.connected_pieces = related_empty_space.connected_pieces
        for point in self.connected_pieces:
            connected_piece = board.HiveGameBoard().pieces[point]
            connected_piece.connected_empty_spaces.remove(self.location)
            connected_piece.connected_pieces.add(self.location)
            if len(connected_piece.connected_pieces) == 5:
                connected_piece.lock()

        self.connected_empty_spaces = related_empty_space.connected_empty_spaces
        for point in self.connected_empty_spaces:
            connected_empty_space = board.HiveGameBoard().empty_spaces[point]
            connected_empty_space.connected_empty_spaces.remove(self.location)
            connected_empty_space.connected_pieces.add(self.location)
            if self.is_white:
                connected_empty_space.num_white_connected += 1
            else:
                connected_empty_space.num_black_connected += 1
            connected_empty_space.update_placement_options()

        # TODO: [Movement] Lock any relevant pieces connected to the new location
        if len(self.connected_pieces) == 1:
            board.HiveGameBoard().pieces[list(self.connected_pieces)[0]].lock()

        # Delete the empty space at this location
        related_empty_space.remove()

        # Add new empty spaces
        all_connected_spaces = self.connected_empty_spaces.union(self.connected_pieces)
        surrounding_locations = {(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x - 1, self.y),
                                 (self.x + 1, self.y),
                                 (self.x, self.y + 1), (self.x + 1, self.y + 1)}
        locations_for_new_empty_spaces = surrounding_locations.difference(all_connected_spaces)

        for point in locations_for_new_empty_spaces:
            emt.EmptySpace(point[0], point[1])

    def formed_loop(self):
        # Check if two pieces are on opposite sides after being places
        return False

    @abstractmethod
    def calc_possible_moves(self):
        pass

    # TODO: [Movement] Implement lock method; currently have a placeholder for testing
    def lock(self):
        type_of_piece = str(type(self)).split('.')[-1][:-2]
        print('{} located at {} has been locked'.format(type_of_piece, self.location))

    # TODO: [Movement] Implement unlock method; currently have a placeholder for testing
    def unlock(self):
        type_of_piece = str(type(self)).split('.')[-1][:-2]
        print('{} located at {} has been unlocked'.format(type_of_piece, self.location))

