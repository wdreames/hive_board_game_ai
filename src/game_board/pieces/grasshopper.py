import src.game_board.piece as p
import src.game_board.board as board


class Grasshopper(p.Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = p.Piece.GRASSHOPPER

    def calc_possible_moves(self):
        # Moves calculated by adding/removing links with other spaces. This is done separately
        self.update_board_moves()
        return self.possible_moves
