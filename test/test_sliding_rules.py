import unittest
import src.game_board.board as board


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        board.HiveGameBoard(new_board=True)

        # Make moves for a sample game
        board.HiveGameBoard().place_piece('Grasshopper', (0, 0))  # White
        board.HiveGameBoard().place_piece('Ant', (-1, -1))  # Black
        board.HiveGameBoard().place_piece('Ant', (0, 1))  # White
        board.HiveGameBoard().place_piece('Queen Bee', (-2, -1))  # Black
        board.HiveGameBoard().place_piece('Queen Bee', (1, 1))  # White
        board.HiveGameBoard().place_piece('Grasshopper', (-3, -1))  # Black
        board.HiveGameBoard().place_piece('Ant', (1, 2))  # White
        board.HiveGameBoard().place_piece('Grasshopper', (-3, 0))  # Black
        board.HiveGameBoard().place_piece('Grasshopper', (0, 2))  # White
        board.HiveGameBoard().place_piece('Ant', (-2, 1))  # Black
        board.HiveGameBoard().place_piece('Grasshopper', (2, 3))  # White

        board.HiveGameBoard().print_board()

    @staticmethod
    def get_all_cannot_move_to_for(location):
        space = board.HiveGameBoard().get_all_spaces()[location]
        cannot_move_set = space.cannot_move_to
        cannot_slide_set = space.sliding_prevented_to.keys()
        return cannot_move_set.union(cannot_slide_set)

    def test_sliding_rules_piece_1(self):
        # Check sample sliding rules for piece at (2, 3) (White Grasshopper)
        expected_cannot_slide_to = set()
        actual_cannot_slide_to = self.get_all_cannot_move_to_for((2, 3))
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_sliding_rules_piece_2(self):
        # Check sample sliding rules for piece at (-2, 1) (Black Ant)
        expected_cannot_slide_to = set()
        actual_cannot_slide_to = self.get_all_cannot_move_to_for((-2, 1))
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_sliding_rules_piece_3(self):
        # Check sample sliding rules for piece at (-1, -1) (Black Ant)
        expected_cannot_slide_to = {(-1, 0)}
        actual_cannot_slide_to = self.get_all_cannot_move_to_for((-1, -1))
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_sliding_rules_emt_spc_1(self):
        # Check sample sliding rules for empty space at (1, 0)
        expected_cannot_slide_to = set()
        actual_cannot_slide_to = self.get_all_cannot_move_to_for((1, 0))
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_sliding_rules_emt_spc_2(self):
        # Check sample sliding rules for empty space at (-1, 0)
        expected_cannot_slide_to = {(-1, -1), (0, 0)}
        actual_cannot_slide_to = self.get_all_cannot_move_to_for((-1, 0))
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_sliding_rules_emt_spc_3(self):
        # Check sample sliding rules for empty space at (-1, 1)
        expected_cannot_slide_to = {(-1, 2)}
        actual_cannot_slide_to = self.get_all_cannot_move_to_for((-1, 1))
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_sliding_rules_emt_spc_4(self):
        # Check sample sliding rules for empty space at (-1, 2)
        expected_cannot_slide_to = {(-1, 1)}
        actual_cannot_slide_to = self.get_all_cannot_move_to_for((-1, 2))
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)


if __name__ == '__main__':
    unittest.main()
