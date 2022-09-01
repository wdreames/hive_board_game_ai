import src.game_board.board as board

from src.game_board.hex_space import HexSpace


class EmptySpace(HexSpace):

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.can_slide_to = set()
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

        self.calc_can_slide_to()
        self.update_placement_options()

    def update_placement_options(self):
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
        board.HiveGameBoard().empty_spaces.pop(self.location)
        if self.location in board.HiveGameBoard().white_locations_to_place:
            board.HiveGameBoard().white_locations_to_place.remove(self.location)
        if self.location in board.HiveGameBoard().black_locations_to_place:
            board.HiveGameBoard().black_locations_to_place.remove(self.location)

        # TODO: [Movement] Logic for pieces that can move here

        for point in self.connected_pieces:
            related_connections = board.HiveGameBoard().pieces[point].connected_empty_spaces
            if point in related_connections:
                related_connections.remove(self.location)
        for point in self.connected_empty_spaces:
            related_connections = board.HiveGameBoard().empty_spaces[point].connected_empty_spaces
            if point in related_connections:
                related_connections.remove(self.location)

        del self

    def calc_can_slide_to(self):
        pass

    def white_can_place(self):
        return not self.num_black_connected and self.num_white_connected > 0

    def black_can_place(self):
        return not self.num_white_connected and self.num_black_connected > 0
