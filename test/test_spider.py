import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestSpiderMove0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        gh = spaces.Piece.GRASSHOPPER
        qb = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(spider, (0, 0))  # White
        game_board.place_piece(ant, (0, 1))  # Black

        game_board.print_board()

    def test_spider1(self):
        # Test Spider at (0, 0)
        expected_possible_moves = {(0, 2)}
        actual_possible_moves = board.HiveGameBoard().pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderMove1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(spider, (0, 0))  # White
        game_board.place_piece(ant, (0, 1))  # Black

        game_board.place_piece(grasshopper, (0, -1))  # White
        game_board.place_piece(queen_bee, (0, 2))  # Black

        game_board.print_board()

    def test_spider1(self):
        # Test Spider at (0, 0)
        expected_possible_moves = {(1, 3), (-1, 2), (0, -2)}
        actual_possible_moves = board.HiveGameBoard().pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderMoveOntoSelf(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(ant, (0, 0))  # White
        game_board.place_piece(queen_bee, (1, 1))  # Black
        game_board.place_piece(beetle, (-1, 0))  # White
        game_board.place_piece(grasshopper, (1, 2))  # Black
        game_board.place_piece(spider, (-1, 1))  # White
        game_board.place_piece(spider, (1, 3))  # Black
        game_board.place_piece(queen_bee, (-1, 2))  # White

        game_board.print_board()

    def test_spider1(self):
        # Test Spider at (-1, 1)
        expected_possible_moves = {(-1, 1), (-1, -1), (-2, 3)}
        actual_possible_moves = board.HiveGameBoard().pieces[(-1, 1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test Spider at (1, 3)
        expected_possible_moves = {(-1, 3), (2, 1)}
        actual_possible_moves = board.HiveGameBoard().pieces[(1, 3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


if __name__ == '__main__':
    unittest.main()
