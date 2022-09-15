from src.game_board.piece import Piece


class Ant(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = 'Ant'

    # TODO: [Movement] Update this to Ant movement (rather than QB mvt)
    def calc_possible_moves(self):
        # Can move to any open space that it can slide to
        unavailable_moves = self.cannot_move_to.union(self.sliding_prevented_to.keys())
        self.possible_moves = self.connected_empty_spaces.difference(unavailable_moves)
        self.update_board_moves()
        return self.possible_moves
