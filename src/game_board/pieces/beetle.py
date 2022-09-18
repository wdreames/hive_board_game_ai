from src.game_board.piece import Piece


class Beetle(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = Piece.BEETLE

    # TODO: [Beetle] Beetle will require a lot of new infrastructure in order to stack on top of pieces
    #       * I could rewrite the remove() and _set_location_to() methods here, but this would be somewhat bad
    #         practice. Although if enough will need to be altered, this could be reasonable.
    #       * OR... I could get a space from HiveGameBoard.get_all_pieces() and gather connections from there. Then I
    #         can implement more specific functionality based on space type.

    def calc_possible_moves(self):
        # Can move to any space that is possible to move to (including on top of pieces)
        self.possible_moves = self.connected_empty_spaces.union(self.connected_pieces).difference(self.cannot_move_to)
        self.update_board_moves()
        return self.possible_moves
