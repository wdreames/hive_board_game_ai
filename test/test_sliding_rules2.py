import unittest
import src.game_board.board as board


class MyTestCase(unittest.TestCase):

    # TODO: [Testing] Will need to add more sliding test cases

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
        board.HiveGameBoard().place_piece('Grasshopper', (1, 0))  # White
        board.HiveGameBoard().place_piece('Ant', (-2, 1))  # Black
        board.HiveGameBoard().place_piece('Grasshopper', (2, 3))  # White
        board.HiveGameBoard().place_piece('Ant', (-1, 2))  # Black

        board.HiveGameBoard().print_board()

    def test_sliding_rules_emt_spc_1(self):
        # Check sample sliding rules for empty space at (0, 2)
        expected_cannot_slide_to = {(-1, 1)}
        actual_cannot_slide_to = board.HiveGameBoard().empty_spaces[(0, 2)].cannot_slide_to
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_sliding_rules_emt_spc_2(self):
        # Check sample sliding rules for empty space at (-1, 1)
        expected_cannot_slide_to = {(0, 2)}
        actual_cannot_slide_to = board.HiveGameBoard().empty_spaces[(-1, 1)].cannot_slide_to
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)


if __name__ == '__main__':
    unittest.main()
