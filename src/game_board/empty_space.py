import src.game_board.board as board

import src.game_board.hex_space as h


class EmptySpace(h.HexSpace):
    """
    Used to represent an empty space containing no pieces on the board. These are used when calculating
    where pieces can be placed or moved.
    """

    def __init__(self, x=0, y=0, connected_pcs=None, connected_emt_spcs=None, sliding_prevented_to=None,
                 cannot_move_to=None):
        """
        Create a new Empty Space at (x, y). This method also allows the Empty Space to connect to any other surrounding
        spaces on the board.

        :param x: int
            x location
        :param y: int
            y location
        :param connected_pcs: set
            Connected pieces to assign to this empty space. If this is None, connected pieces will be calculated
        :param connected_emt_spcs: set
                Connected empty pieces to assign to this empty space. If this is None, connected empty spaces will be
                calculated.
        """
        super().__init__(x, y)
        self.pieces_that_can_move_here = set()
        self.num_white_connected = 0
        self.num_black_connected = 0

        board.HiveGameBoard().empty_spaces[self.location] = self

        # TODO: [Formatting] Clean this up

        if connected_pcs is None or connected_emt_spcs is None:
            # Check surrounding spaces and connect to them
            for space_location in self.get_surrounding_locations():
                all_spaces = board.HiveGameBoard().get_all_spaces()
                if space_location in all_spaces:
                    all_spaces[space_location].add_connection_to_empty_space(self.location)
        else:
            # Update connections
            # Assumes the other pieces/empty_spaces will be connected to this empty space on their own
            self.connected_pieces = connected_pcs
            self.connected_empty_spaces = connected_emt_spcs
            self.sliding_prevented_to = sliding_prevented_to
            self.cannot_move_to = cannot_move_to

            # TODO: [Efficiency] If the pieces also store this info, this loop would be unecessary
            # Check which player can place here
            for piece in self.connected_pieces:
                if board.HiveGameBoard().pieces[piece].is_white:
                    self.num_white_connected += 1
                else:
                    self.num_black_connected += 1
            self.prepare_for_update()

    def update(self):
        if len(self.connected_pieces) == 0:
            self.remove()
            return

        super().update()
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

        for space_location in self.connected_pieces.union(self.connected_empty_spaces):
            board.HiveGameBoard().get_all_spaces()[space_location].remove_connection_to_empty_space(self.location)

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
        super().add_connection_to_piece(location)
        if board.HiveGameBoard().pieces[location].is_white:
            self.num_white_connected += 1
        else:
            self.num_black_connected += 1

    def remove_connection_to_piece(self, location):
        super().remove_connection_to_piece(location)

        if board.HiveGameBoard().pieces[location].is_white:
            self.num_white_connected -= 1
        else:
            self.num_black_connected -= 1

        self.prepare_for_update()

    def add_connection_to_empty_space(self, location):
        super().add_connection_to_empty_space(location)
        board.HiveGameBoard().empty_spaces[location].connected_empty_spaces.add(self.location)

    def remove_connection_to_empty_space(self, location):
        super().remove_connection_to_empty_space(location)

    def __str__(self):
        return_str = 'Information for EmptySpace at {}:\n'.format(self.location)
        return_str += 'connected_pieces: {}\n'.format(self.connected_pieces)
        return_str += 'connected_empty_spaces: {}\n'.format(self.connected_empty_spaces)
        return_str += 'cannot_move_to: {}\n'.format(self.cannot_move_to)
        return_str += 'sliding_prevented_to: {}\n'.format(self.sliding_prevented_to)
        return_str += f'pieces_that_can_move_here: {self.pieces_that_can_move_here}\n'
        return_str += f'num_white_connected: {self.num_white_connected}\n'
        return_str += f'num_black_connected: {self.num_black_connected}\n'

        return return_str
