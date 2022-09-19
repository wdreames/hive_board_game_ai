from abc import abstractmethod
import src.game_board.board as board


class HexSpace:
    """
    This is a single space on the Hive game board. This is the superclass for Pieces and Empty Spaces
    """

    def __init__(self, x=0, y=0):
        """
        Initialize values for a space on the board

        :param x: int
            x location
        :param y: int
            y location
        """
        self.name = ''
        self.x = x
        self.y = y
        self.location = (self.x, self.y)
        self.connected_pieces = set()
        self.connected_empty_spaces = set()
        self.cannot_move_to = set()
        self.sliding_prevented_to = dict()

        self.grasshopper_links = set()

    def prepare_for_update(self):
        board.HiveGameBoard().spaces_requiring_updates.add(self.location)

    def update(self):
        self.update_cannot_move_to()

    def update_cannot_move_to(self):
        # If pieces at specific locations do not exist, you cannot slide in certain directions without disconnecting
        # from the Hive
        x = self.x
        y = self.y

        self._add_to_cannot_move_to((x, y - 1), (x - 1, y - 1), (x + 1, y))
        self._add_to_cannot_move_to((x + 1, y), (x, y - 1), (x + 1, y + 1))
        self._add_to_cannot_move_to((x + 1, y + 1), (x + 1, y), (x, y + 1))
        self._add_to_cannot_move_to((x, y + 1), (x - 1, y), (x + 1, y + 1))
        self._add_to_cannot_move_to((x - 1, y), (x - 1, y - 1), (x, y + 1))
        self._add_to_cannot_move_to((x - 1, y - 1), (x, y - 1), (x - 1, y))

    def _add_to_cannot_move_to(self, loc, loc_check1, loc_check2):
        pieces = board.HiveGameBoard().pieces
        if {loc_check1, loc_check2}.isdisjoint(pieces) and loc in board.HiveGameBoard().empty_spaces:
            self.cannot_move_to.add(loc)
        elif loc in self.cannot_move_to:
            self.cannot_move_to.remove(loc)

    @staticmethod
    def dir_from_a_to_b(piece_a, piece_b):
        print('Calling Direction')
        print(f'Piece a: {piece_a}')
        print(f'Piece b: {piece_b}')
        x_diff = piece_b[0] - piece_a[0]
        y_diff = piece_b[1] - piece_a[1]
        divisor = max(abs(x_diff), abs(y_diff))
        if divisor == 0:
            print('Direction = 0')
            return 0, 0
        else:
            print(f'Direction = {x_diff // divisor, y_diff // divisor}')
            return x_diff // divisor, y_diff // divisor

    @staticmethod
    def get_next_space_in_dir(start_location, direction):
        # If the direction is 0, this would return the same location, possibly leading to an infinite loop
        # if direction == (0, 0):
        #     raise ValueError('Direction cannot be (0, 0)')

        # print(f'Start location: {start_location}')
        # print(f'Direction: {direction}')
        new_location = (start_location[0] + direction[0], start_location[1] + direction[1])
        # print(f'New Location: {new_location}')
        if new_location in board.HiveGameBoard().get_all_spaces():
            return new_location
        else:
            return None

    def add_link_to_grasshopper(self, grasshopper_loc):
        self.grasshopper_links.add(grasshopper_loc)

    def remove_link_to_grasshopper(self, grasshopper_loc):
        # if grasshopper_loc in self.grasshopper_links:
        self.grasshopper_links.remove(grasshopper_loc)

    def add_gh_links_in_direction(self, grasshopper_loc, direction, start_loc=None):
        print('=' * 50)
        print(f'Adding GH Links for {self.name} at {self.location}')
        if start_loc is None:
            next_loc = grasshopper_loc
        else:
            next_loc = start_loc

        all_spaces = board.HiveGameBoard().get_all_spaces()
        while next_loc is not None:
            all_spaces[next_loc].add_link_to_grasshopper(grasshopper_loc)
            print(f'Added link to {all_spaces[next_loc].name} at {all_spaces[next_loc].location}')
            if next_loc in board.HiveGameBoard().empty_spaces:
                return

            next_loc = self.get_next_space_in_dir(next_loc, direction)
            print(f'The next location to add is {next_loc}')

    def remove_gh_links_in_direction(self, grasshopper_loc, direction, start_loc=None):
        print('=' * 50)
        print(f'Removing GH Links for {self.name} at {self.location}')
        if start_loc is None or start_loc == grasshopper_loc:
            next_loc = self.get_next_space_in_dir(grasshopper_loc, direction)
        else:
            next_loc = start_loc

        all_spaces = board.HiveGameBoard().get_all_spaces()
        while next_loc is not None and grasshopper_loc in all_spaces[next_loc].grasshopper_links:
            all_spaces[next_loc].remove_link_to_grasshopper(grasshopper_loc)
            next_loc = self.get_next_space_in_dir(next_loc, direction)

    def get_surrounding_locations(self):
        return {(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x - 1, self.y),
                (self.x + 1, self.y), (self.x, self.y + 1), (self.x + 1, self.y + 1)}

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def add_connection_to_piece(self, location):
        self.connected_pieces.add(location)
        self.prepare_for_update()

    @abstractmethod
    def remove_connection_to_piece(self, location):
        self.connected_pieces.remove(location)
        self.prepare_for_update()

    @abstractmethod
    def add_connection_to_empty_space(self, location):
        self.connected_empty_spaces.add(location)
        self.prepare_for_update()

    @abstractmethod
    def remove_connection_to_empty_space(self, location):
        self.connected_empty_spaces.remove(location)
        self.prepare_for_update()
