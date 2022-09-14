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
        self.x = x
        self.y = y
        self.location = (self.x, self.y)
        self.connected_pieces = set()
        self.connected_empty_spaces = set()
        self.cannot_move_to = set()
        self.sliding_prevented_to = dict()

    def update_cannot_move_to(self):
        # If pieces at specific locations do not exist, you cannot slide in certain directions without disconnecting
        # from the Hive
        x = self.x
        y = self.y

        self._add_to_cannot_move_to((x, y - 1),     (x - 1, y - 1), (x + 1, y))
        self._add_to_cannot_move_to((x + 1, y),     (x, y - 1),     (x + 1, y + 1))
        self._add_to_cannot_move_to((x + 1, y + 1), (x + 1, y),     (x, y + 1))
        self._add_to_cannot_move_to((x, y + 1),     (x - 1, y),     (x + 1, y + 1))
        self._add_to_cannot_move_to((x - 1, y),     (x - 1, y - 1), (x, y + 1))
        self._add_to_cannot_move_to((x - 1, y - 1), (x, y - 1),     (x - 1, y))

    def _add_to_cannot_move_to(self, loc, loc_check1, loc_check2):
        pieces = board.HiveGameBoard().pieces
        if {loc_check1, loc_check2}.isdisjoint(pieces):
            self.cannot_move_to.add(loc)
        elif loc in self.cannot_move_to:
            self.cannot_move_to.remove(loc)

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def add_connection_to_piece(self, location):
        self.connected_pieces.add(location)
        self.update_cannot_move_to()

    @abstractmethod
    def remove_connection_to_piece(self, location):
        self.connected_pieces.remove(location)
        self.update_cannot_move_to()

    @abstractmethod
    def add_connection_to_empty_space(self, location):
        self.connected_empty_spaces.add(location)

    @abstractmethod
    def remove_connection_to_empty_space(self, location):
        # If an error occurs here, the program can likely be made to be more efficient. Don't use the following if stmt
        # if location in self.connected_empty_spaces:
        self.connected_empty_spaces.remove(location)
