import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestToStrings(unittest.TestCase):
    """
    The __str__() functions in each class are only used for debugging and are not used during the game.
    This test case only serves to add these functions to the test's code coverage.
    """

    def test_str(self):
        game_board = board.HiveGameBoard()
        game_board.place_piece(spaces.Piece.ANT, (0, 0))

        self.assertTrue(game_board.__str__())
        self.assertTrue(game_board.pieces[(0, 0)].__str__())
        self.assertTrue(game_board.empty_spaces[(1, 0)].__str__())


if __name__ == '__main__':
    unittest.main()
