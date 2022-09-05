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
        self.cannot_slide_to = set()

    def _update_can_slide_to(self):
        """
        Method used to determine which spaces this space can slide into. Comment diagrams are displayed
        for each type of movement to help show the conditions required to slide in that direction.
        This method sets new values to self.can_slide_to
        """

        # TODO: [Efficiency] There may be a better way to update this as the game progresses
        self.can_slide_to.clear()

        # Storing shorter names for variables
        x = self.x
        y = self.y
        pieces = self.connected_pieces
        emt_spcs = self.connected_empty_spaces

        # For comment diagrams, X = a connected piece, * = this space

        # Up
        # | X |   |  or  |   |   |
        # |   | * |      | X | * |
        if (x, y - 1) in emt_spcs and ((x - 1, y - 1) in pieces or (x + 1, y) in pieces):
            self.can_slide_to.add((x, y - 1))
        # Right
        # | X |   |  or  | * |   |
        # | * |   |      |   | X |
        if (x + 1, y) in emt_spcs and ((x, y - 1) in pieces or (x + 1, y + 1) in pieces):
            self.can_slide_to.add((x + 1, y))
        # Down
        # | X | * |  or  | * |   |
        # |   |   |      |   | X |
        if (x, y + 1) in emt_spcs and ((x - 1, y) in pieces or (x + 1, y + 1) in pieces):
            self.can_slide_to.add((x, y + 1))
        # Left
        # |   | * |  or  | X |   |
        # |   | X |      |   | * |
        if (x - 1, y) in emt_spcs and ((x - 1, y - 1) in pieces or (x, y + 1) in pieces):
            self.can_slide_to.add((x - 1, y))
        # Diagonal up-left
        # |   | X |  xor |   |   |
        # |   | * |      | X | * |
        if (x - 1, y - 1) in emt_spcs and ((x, y - 1) in pieces or (x - 1, y) in pieces) and not (
                (x, y - 1) in pieces and (x - 1, y) in pieces
        ):
            self.can_slide_to.add((x - 1, y - 1))
        # Diagonal down-right
        # | * | X |  xor | * |   |
        # |   |   |      | X |   |
        if (x + 1, y + 1) in emt_spcs and ((x + 1, y) in pieces or (x, y + 1) in pieces) and not (
                (x + 1, y) in pieces and (x, y + 1) in pieces
        ):
            self.can_slide_to.add((x + 1, y + 1))
