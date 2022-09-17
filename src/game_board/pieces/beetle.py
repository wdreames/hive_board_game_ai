from src.game_board.piece import Piece


class Beetle(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = Piece.BEETLE
        self.stacked_piece = None

    # TODO: [Beetle] Beetle will require a lot of new infrastructure in order to stack on top of pieces
    #       * I could rewrite the remove() and _set_location_to() methods here. This would be somewhat bad
    #         practice, though.
    #       * OR... I could get a space from HiveGameBoard.get_all_pieces() and gather connections from there. Then I
    #         can implement more specific functionality based on space type.

    def remove(self, is_beetle=True):
        super().remove(is_beetle=True)

    def _set_location_to(self, new_location, is_beetle=True):
        super()._set_location_to(new_location, is_beetle=True)

    def calc_possible_moves(self):
        # Can move to any space that is possible to move to (including on top of pieces)
        unavailable_moves = self.cannot_move_to.union
        self.possible_moves = self.connected_empty_spaces.union(self.connected_pieces).difference(unavailable_moves)
        self.update_board_moves()
        return self.possible_moves
