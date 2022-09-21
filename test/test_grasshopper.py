import unittest
import src.game_board.board as game_board
import src.game_board.spaces as spcs


class TestGrasshopper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.board = game_board.HiveGameBoard(new_board=True)

        cls.board.perform_action(cls.board.PLACE_PIECE, (0, 0), piece_type=spcs.Piece.GRASSHOPPER)
        cls.board.perform_action(cls.board.PLACE_PIECE, (1, 0), piece_type=spcs.Piece.GRASSHOPPER)
        cls.board.perform_action(cls.board.PLACE_PIECE, (-1, 0), piece_type=spcs.Piece.ANT)

    def test_1_moveset_1(self):
        # Testing grasshopper as (0, 0)
        expected_moves = {(-2, 0), (2, 0)}
        actual_moves = self.board.white_possible_moves[(0, 0)]
        self.assertEqual(expected_moves, actual_moves)

    def test_1_moveset_2(self):
        # Testing grasshopper at (1, 0)
        expected_moves = {(-2, 0)}
        actual_moves = self.board.black_possible_moves[(1, 0)]
        self.assertEqual(expected_moves, actual_moves)

    def test_2_movement_and_movesets(self):
        self.board.perform_action(self.board.MOVE_PIECE, (1, 0), new_location=(-2, 0))

        expected_moves_0_0 = {(-3, 0)}
        actual_moves_0_0 = self.board.white_possible_moves[(0, 0)]
        self.assertEqual(expected_moves_0_0, actual_moves_0_0)

        expected_moves_negative_2_0 = {(1, 0)}
        actual_moves_negative_2_0 = self.board.black_possible_moves[(-2, 0)]
        self.assertEqual(expected_moves_negative_2_0, actual_moves_negative_2_0)


if __name__ == '__main__':
    unittest.main()
