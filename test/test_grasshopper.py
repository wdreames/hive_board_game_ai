import unittest
import src.game.board as game_board
import src.game.spaces as spcs


class TestGrasshopper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.board = game_board.HiveGameBoard()

        cls.board.perform_action_helper(cls.board.PLACE_PIECE, (0, 0), piece_type=spcs.Piece.GRASSHOPPER)
        cls.board.perform_action_helper(cls.board.PLACE_PIECE, (1, 0), piece_type=spcs.Piece.GRASSHOPPER)
        cls.board.perform_action_helper(cls.board.PLACE_PIECE, (-1, 0), piece_type=spcs.Piece.QUEEN_BEE)

        cls.board.place_piece(spcs.Piece.QUEEN_BEE, (2, 1))
        cls.board.move_piece((-1, 0), (-1, -1))
        cls.board.move_piece((2, 1), (1, 1))
        cls.board.move_piece((-1, -1), (-1, 0))

        cls.board.print_board()

    def test_1_moveset_1(self):
        # Testing grasshopper as (0, 0)
        expected_moves = {(-2, 0), (2, 0), (2, 2)}
        actual_moves = self.board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_moves, actual_moves)

    def test_1_moveset_2(self):
        # Testing grasshopper at (1, 0)
        expected_moves = {(-2, 0), (1, 2)}
        actual_moves = self.board.pieces[(1, 0)].possible_moves
        self.assertEqual(expected_moves, actual_moves)

    def test_2_movement_and_movesets(self):
        self.board.perform_action_helper(self.board.MOVE_PIECE, (1, 0), new_location=(-2, 0))

        self.board.print_board()

        expected_moves_0_0 = {(-3, 0), (2, 2)}
        actual_moves_0_0 = self.board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_moves_0_0, actual_moves_0_0)

        expected_moves_negative_2_0 = {(1, 0)}
        actual_moves_negative_2_0 = self.board.pieces[(-2, 0)].possible_moves
        self.assertEqual(expected_moves_negative_2_0, actual_moves_negative_2_0)


if __name__ == '__main__':
    unittest.main()
