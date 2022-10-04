import unittest
import src.game.board as board


class TestSlidingRulesNoMvt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)

        # Making sure there are enough pieces to be placed for my test cases
        game_board.white_pieces_to_place = {
            'Ant': 5,
            'Queen Bee': 1,
            'Grasshopper': 5
        }
        game_board.black_pieces_to_place = {
            'Ant': 5,
            'Queen Bee': 1,
            'Grasshopper': 5
        }

        # Make moves for a sample game
        game_board.place_piece('Ant',            (0, 0))  # White
        game_board.place_piece('Ant',            (0, -1))  # Black
        game_board.place_piece('Ant',            (-1, 0))  # White
        game_board.place_piece('Queen Bee',      (0, -2))  # Black
        game_board.place_piece('Ant',            (-2, 0))  # White
        game_board.place_piece('Ant',            (1, -2))  # Black

        game_board.place_piece('Queen Bee',      (-3, -1))  # White
        game_board.place_piece('Ant',            (2, -2))  # Black
        game_board.place_piece('Grasshopper',    (-3, -2))  # White
        game_board.place_piece('Grasshopper',    (3, -1))  # Black
        game_board.place_piece('Grasshopper',    (-3, -3))  # White
        game_board.place_piece('Grasshopper',    (3, 0))  # Black
        game_board.place_piece('Grasshopper',    (-2, -3))  # White

        game_board.print_board()

    def test_both_1(self):
        # Use sample empty space at (2, 0)
        expected_cannot_move_to = {(1, 0), (1, -1), (2, 1), (3, 0)}
        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(2, 0)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)

        expected_cannot_slide_to = set()
        actual_cannot_slide_to = board.HiveGameBoard().get_all_spaces()[(2, 0)].sliding_prevented_to.keys()
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)

        # Place a new piece at (2,0). Movement limitations should remain unchanged
        board.HiveGameBoard().place_piece('Grasshopper', (2, 0))  # Black

        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(2, 0)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)

        actual_cannot_slide_to = board.HiveGameBoard().get_all_spaces()[(2, 0)].sliding_prevented_to.keys()
        self.assertEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_closed_gap_1(self):
        # Use sample empty space at (-1, -1)
        expected_cannot_slide_to = {
            (0, 0): {(-1, 0), (0, -1)}
        }
        actual_cannot_slide_to = board.HiveGameBoard().get_all_spaces()[(-1, -1)].sliding_prevented_to
        self.assertDictEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_floating_space_1(self):
        # Use sample empty space at (-1, -1)
        expected_cannot_move_to = {(-2, -2)}
        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(-1, -1)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)

        # Use sample empty space at (-2, -2)
        expected_cannot_move_to = {(-1, -1)}
        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(-2, -2)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)

    def test_closed_gap_2(self):
        # Use sample piece at (0, 0)
        expected_cannot_slide_to = {
            (-1, -1): {(-1, 0), (0, -1)}
        }
        actual_cannot_slide_to = board.HiveGameBoard().get_all_spaces()[(0, 0)].sliding_prevented_to
        self.assertDictEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_floating_space_2(self):
        # Use sample piece at (0, 0)
        expected_cannot_move_to = {(1, 1), (-1, 0), (0, -1)}
        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(0, 0)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)

    def test_closed_gap_3(self):
        # Use sample empty space at (-2, -1)
        expected_cannot_slide_to = {
            (-3, -1): {(-3, -2), (-2, 0)},
            (-2, 0): {(-3, -1), (-1, 0)}
        }
        actual_cannot_slide_to = board.HiveGameBoard().get_all_spaces()[(-2, -1)].sliding_prevented_to
        self.assertDictEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_floating_space_3(self):
        # Use sample empty space at (-2, -1)
        expected_cannot_move_to = set()
        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(-2, -1)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)

    def test_closed_gap_4(self):
        # Use sample piece at (-3, -1)
        expected_cannot_slide_to = {
            (-2, -1): {(-3, -2), (-2, 0)}
        }
        actual_cannot_slide_to = board.HiveGameBoard().get_all_spaces()[(-3, -1)].sliding_prevented_to
        self.assertDictEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_floating_space_4(self):
        # Use sample empty space at (-3, -1)
        expected_cannot_move_to = {(-2, 0), (-4, -1), (-3, -2)}
        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(-3, -1)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)

    def test_closed_gap_5(self):
        # Use sample empty space at (-2, -0)
        expected_cannot_slide_to = {
            (-2, -1): {(-3, -1), (-1, 0)}
        }
        actual_cannot_slide_to = board.HiveGameBoard().get_all_spaces()[(-2, 0)].sliding_prevented_to
        self.assertDictEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_floating_space_5(self):
        # Use sample empty space at (-2, 0)
        expected_cannot_move_to = {(-1, 0), (-2, 1), (-3, -1)}
        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(-2, 0)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)

    def test_closed_gap_6(self):
        # Use sample empty space at (-1, -3)
        expected_cannot_slide_to = {
            (-1, -2): {(-2, -3), (0, -2)}
        }
        actual_cannot_slide_to = board.HiveGameBoard().get_all_spaces()[(-1, -3)].sliding_prevented_to
        self.assertDictEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_floating_space_6(self):
        # Use sample empty space at (-1, -3)
        expected_cannot_move_to = {(-2, -3), (-1, -4), (0, -2)}
        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(-1, -3)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)

    def test_closed_gap_7(self):
        # Use sample piece at (0, -2)
        expected_cannot_slide_to = {
            (1, -1): {(0, -1), (1, -2)}
        }
        actual_cannot_slide_to = board.HiveGameBoard().get_all_spaces()[(0, -2)].sliding_prevented_to
        self.assertDictEqual(expected_cannot_slide_to, actual_cannot_slide_to)

    def test_floating_space_7(self):
        # Use sample empty space at (0, -2)
        expected_cannot_move_to = {(0, -1), (1, -2), (-1, -3)}
        actual_cannot_move_to = board.HiveGameBoard().get_all_spaces()[(0, -2)].cannot_move_to
        self.assertEqual(expected_cannot_move_to, actual_cannot_move_to)


if __name__ == '__main__':
    unittest.main()
