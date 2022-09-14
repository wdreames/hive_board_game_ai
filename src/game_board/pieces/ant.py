from src.game_board.piece import Piece


class Ant(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = 'Ant'

    def calc_possible_moves(self):
        pass
