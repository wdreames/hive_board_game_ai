from src.game_board.piece import Piece
import src.game_board.board as board

class QueenBee(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        if is_white:
            board.HiveGameBoard().white_queen_location = self.location
        else:
            board.HiveGameBoard().black_queen_location = self.location

    def calc_possible_moves(self):
        pass
