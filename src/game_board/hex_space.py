
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
