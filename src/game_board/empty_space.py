import src.game_board.board as board

from src.game_board.hex_space import HexSpace


class EmptySpace(HexSpace):
    """
    Used to represent an empty space containing no pieces on the board. These are used when calculating
    where pieces can be placed or moved.
    """

    def __init__(self, x=0, y=0):
        """
        Create a new Empty Space at (x, y). This method also allows the Empty Space to connect to any other surrounding
        spaces on the board.

        :param x: int
            x location
        :param y: int
            y location
        """
        super().__init__(x, y)
        self.pieces_that_can_move_here = set()
        self.num_white_connected = 0
        self.num_black_connected = 0

        board.HiveGameBoard().empty_spaces[self.location] = self

        # Check surrounding spaces and connect to them
        for space_location in [(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x - 1, self.y),
                               (self.x + 1, self.y), (self.x, self.y + 1), (self.x + 1, self.y + 1)]:
            all_spaces = board.HiveGameBoard().get_all_spaces()
            if space_location in all_spaces:
                all_spaces[space_location].add_connection_to_empty_space(self.location)

    def update_placement_options(self):
        """
        Determines if white or black pieces can be placed here based on the number of connected pieces.
        If only white pieces have been connected, a white piece can be placed here.
        If only black pieces have been connected, a black piece can be placed here.
        Otherwise, no pieces can be placed here.
        """
        if self.white_can_place():
            board.HiveGameBoard().white_locations_to_place.add(self.location)
            if self.location in board.HiveGameBoard().black_locations_to_place:
                board.HiveGameBoard().black_locations_to_place.remove(self.location)
        elif self.black_can_place():
            board.HiveGameBoard().black_locations_to_place.add(self.location)
            if self.location in board.HiveGameBoard().white_locations_to_place:
                board.HiveGameBoard().white_locations_to_place.remove(self.location)
        else:
            if self.location in board.HiveGameBoard().black_locations_to_place:
                board.HiveGameBoard().black_locations_to_place.remove(self.location)
            if self.location in board.HiveGameBoard().white_locations_to_place:
                board.HiveGameBoard().white_locations_to_place.remove(self.location)

    def remove(self):
        """
        Removes this empty space from the game board. This also removes this spot from each player's list of locations
        to place pieces, and disconnects any previously connected spaces.
        """
        board.HiveGameBoard().empty_spaces.pop(self.location)
        if self.location in board.HiveGameBoard().white_locations_to_place:
            board.HiveGameBoard().white_locations_to_place.remove(self.location)
        if self.location in board.HiveGameBoard().black_locations_to_place:
            board.HiveGameBoard().black_locations_to_place.remove(self.location)

        for space_location in self.connected_pieces.union(self.connected_empty_spaces):
            board.HiveGameBoard().get_all_spaces()[space_location].remove_connection_to_empty_space(self.location)

        # TODO: [Movement] Logic for pieces that can move here

        del self

    def white_can_place(self):
        """
        Checks if white can place a piece on this empty space

        :return: bool
            True if white can place a piece here; False otherwise
        """
        return not self.num_black_connected

    def black_can_place(self):
        """
        Checks if black can place a piece on this empty space

        :return: bool
            True if black can place a piece here; False otherwise
        """
        return not self.num_white_connected

    def add_connection_to_piece(self, location):
        self.connected_pieces.add(location)
        if board.HiveGameBoard().pieces[location].is_white:
            self.num_white_connected += 1
        else:
            self.num_black_connected += 1
        self.update_placement_options()

    def remove_connection_to_piece(self, location):
        pass

    def add_connection_to_empty_space(self, location):
        self.connected_empty_spaces.add(location)
        board.HiveGameBoard().empty_spaces[location].connected_empty_spaces.add(self.location)

    def remove_connection_to_empty_space(self, location):
        # If an error occurs here, the program can likely be made to be more efficient. Don't use the following if stmt
        # if location in self.connected_empty_spaces:
        self.connected_empty_spaces.remove(location)
