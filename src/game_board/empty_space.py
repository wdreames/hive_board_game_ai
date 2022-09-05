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
        for point in [(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x - 1, self.y), (self.x + 1, self.y),
                      (self.x, self.y + 1), (self.x + 1, self.y + 1)]:
            if point in board.HiveGameBoard().pieces:
                related_piece = board.HiveGameBoard().pieces[point]
                self.connected_pieces.add(point)
                related_piece.connected_empty_spaces.add(self.location)

                # Add to count of that piece's color
                if related_piece.is_white:
                    self.num_white_connected += 1
                else:
                    self.num_black_connected += 1

            elif point in board.HiveGameBoard().empty_spaces:
                self.connected_empty_spaces.add(point)
                board.HiveGameBoard().empty_spaces[point].connected_empty_spaces.add(self.location)

        self.update_placement_options()

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

        # TODO: [Movement] Logic for pieces that can move here

        # TODO: [Efficiency] Think about whether or not this section is necessary. It is missing in code coverage.
        #       Assuming that this method is only called after piece is placed or moved, this won't be needed.
        # for point in self.connected_pieces:
        #     related_connections = board.HiveGameBoard().pieces[point].connected_empty_spaces
        #     if point in related_connections:
        #         related_connections.remove(self.location)
        # for point in self.connected_empty_spaces:
        #     related_connections = board.HiveGameBoard().empty_spaces[point].connected_empty_spaces
        #     if point in related_connections:
        #         related_connections.remove(self.location)

        del self

    def white_can_place(self):
        """
        Checks if white can place a piece on this empty space

        :return: bool
            True if white can place a piece here; False otherwise
        """
        return not self.num_black_connected and self.num_white_connected > 0

    def black_can_place(self):
        """
        Checks if black can place a piece on this empty space

        :return: bool
            True if black can place a piece here; False otherwise
        """
        return not self.num_white_connected and self.num_black_connected > 0
