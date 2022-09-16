from src.game_board.piece import Piece
import src.game_board.board as board


class QueenBee(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = Piece.QUEEN_BEE

    def update(self):
        super().update()
        self.update_board_location()

    def update_board_location(self):
        if self.is_white:
            board.HiveGameBoard().white_queen_location = self.location
        else:
            board.HiveGameBoard().black_queen_location = self.location

    def calc_possible_moves(self):
        # Can move to any open space that it can slide to
        unavailable_moves = self.cannot_move_to.union(self.sliding_prevented_to.keys())
        self.possible_moves = self.connected_empty_spaces.difference(unavailable_moves)
        self.update_board_moves()
        return self.possible_moves
