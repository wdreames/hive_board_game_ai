import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestSpiderBoard1Move0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(spider, (0, 0))  # White
        game_board.place_piece(queen_bee, (0, 1))  # Black

        game_board.print_board()

    def test_spider1(self):
        # Test Spider at (0, 0)
        expected_possible_moves = {(0, 2)}
        actual_possible_moves = board.HiveGameBoard().pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard1Move1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(spider, (0, 0))  # White
        game_board.place_piece(queen_bee, (0, 1))  # Black

        game_board.place_piece(grasshopper, (0, -1))  # White
        game_board.place_piece(ant, (0, 2))  # Black

        game_board.print_board()

    def test_spider1(self):
        # Test Spider at (0, 0)
        expected_possible_moves = {(0, -2), (-1, 2), (1, 3)}
        actual_possible_moves = board.HiveGameBoard().pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard1Move2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(spider, (0, 0))  # White
        game_board.place_piece(queen_bee, (0, 1))  # Black

        game_board.place_piece(grasshopper, (0, -1))  # White
        game_board.place_piece(ant, (0, 2))  # Black

        game_board.place_piece(beetle, (1, 0))  # Black
        game_board.move_piece((0, 2), (0, -2))  # White

        game_board.print_board()

    def test_spider1(self):
        # Test Spider at (0, 0)
        expected_possible_moves = {(0, 2), (-1, -3)}
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

    # TODO: [Spider] This fails because updates to sliding rules do not update Spider movement
    def test_spider1(self):
        # Test Spider at (-1, 1)
        expected_possible_moves = {(-1, 1), (-1, -1), (-1, 3)}
        actual_possible_moves = board.HiveGameBoard().pieces[(-1, 1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

        # Move onto itself
        board.HiveGameBoard().move_piece((-1, 1), (-1, 1))
        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test Spider at (1, 3)
        expected_possible_moves = {(-1, 3), (2, 1)}
        actual_possible_moves = board.HiveGameBoard().pieces[(1, 3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard2Move0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(beetle, (0, 0))
        game_board.place_piece(grasshopper, (1, 0))
        game_board.place_piece(spider, (-1, -1))
        game_board.place_piece(spider, (2, 0))

        game_board.print_board()

    def test_spider1(self):
        # Test spider at (-1, -1)
        expected_possible_moves = {(2, -1), (1, 1)}
        actual_possible_moves = board.HiveGameBoard().pieces[(-1, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test spider at (2, 0)
        expected_possible_moves = {(-1, -2), (0, 1)}
        actual_possible_moves = board.HiveGameBoard().pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard2Move1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(beetle, (0, 0))
        game_board.place_piece(grasshopper, (1, 0))
        game_board.place_piece(spider, (-1, -1))
        game_board.place_piece(spider, (2, 0))

        game_board.print_board()

        game_board.move_piece((-1, -1), (2, -1))

        game_board.print_board()

    def test_spider1(self):
        # Test spider at (2, -1)
        expected_possible_moves = {(-1, -1), (2, 1)}
        actual_possible_moves = board.HiveGameBoard().pieces[(2, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test spider at (2, 0)
        expected_possible_moves = {(2, -2), (0, 1)}
        actual_possible_moves = board.HiveGameBoard().pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard2Move2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(beetle, (0, 0))
        game_board.place_piece(grasshopper, (1, 0))
        game_board.place_piece(spider, (-1, -1))
        game_board.place_piece(spider, (2, 0))

        game_board.move_piece((-1, -1), (2, -1))

        game_board.place_piece(grasshopper, (3, 1))
        game_board.place_piece(queen_bee, (-1, 0))

        game_board.print_board()

    def test_spider1(self):
        # Test spider at (2, -1)
        expected_possible_moves = {(-1, -1), (4, 2)}
        actual_possible_moves = board.HiveGameBoard().pieces[(2, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test spider at (2, 0)
        expected_possible_moves = set()
        actual_possible_moves = board.HiveGameBoard().pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard2Move3(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(beetle, (0, 0))
        game_board.place_piece(grasshopper, (1, 0))
        game_board.place_piece(spider, (-1, -1))
        game_board.place_piece(spider, (2, 0))

        game_board.move_piece((-1, -1), (2, -1))

        game_board.place_piece(grasshopper, (3, 1))
        game_board.place_piece(queen_bee, (-1, 0))

        game_board.move_piece((3, 1), (1, -1))

        game_board.print_board()

    def test_spider1(self):
        # Test spider at (2, -1)
        expected_possible_moves = {(0, -1), (2, 1)}
        actual_possible_moves = board.HiveGameBoard().pieces[(2, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test spider at (2, 0)
        expected_possible_moves = {(2, -2), (0, 1)}
        actual_possible_moves = board.HiveGameBoard().pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderOverlappingPaths(unittest.TestCase):

    @staticmethod
    def setup_spider_test_board():
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(ant, (0, 0))  # White
        game_board.place_piece(ant, (0, 1))  # Black
        game_board.place_piece(ant, (0, -1))  # White
        game_board.place_piece(ant, (0, 2))  # Black
        game_board.place_piece(ant, (0, -2))  # White
        game_board.place_piece(ant, (0, 3))  # Black

        game_board.place_piece(queen_bee, (-1, -3))  # White
        game_board.place_piece(queen_bee, (-1, 3))  # Black

        game_board.place_piece(beetle, (-2, -4))  # White
        game_board.place_piece(beetle, (-2, 3))  # Black
        game_board.place_piece(beetle, (-3, -4))  # White
        game_board.place_piece(beetle, (-3, 2))  # Black

        game_board.place_piece(spider, (-3, -3))  # White
        game_board.place_piece(spider, (-3, 1))  # Black

        game_board.place_piece(grasshopper, (-3, -2))  # White
        game_board.place_piece(grasshopper, (-3, 0))  # Black

        game_board.place_piece(spider, (-4, -4))  # White - this is the Spider being tested
        game_board.place_piece(grasshopper, (1, 2))  # Black

        game_board.print_board()

    def test_spider_before_move(self):
        self.setup_spider_test_board()
        # Test Spider at (-4, -4) before moving
        expected_possible_moves = {(-3, -1), (-2, -5)}
        actual_possible_moves = board.HiveGameBoard().pieces[(-4, -4)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider_after_move(self):
        self.setup_spider_test_board()
        board.HiveGameBoard().move_piece((-4, -4), (-3, -1))

        # Check the moves for the Spider after moving to (-3, -1)
        expected_possible_moves = {(-4, -4), (-4, 1), (-2, -3), (-2, 2)}
        actual_possible_moves = board.HiveGameBoard().pieces[(-3, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_3_spider_moves_updated(self):
        self.setup_spider_test_board()
        board.HiveGameBoard().move_piece((-4, -4), (-3, -1))

        # Move the grasshopper from (1, 2) to (-1, 0). This should update the Spiders set of possible moves.
        board.HiveGameBoard().move_piece((1, 2), (-1, 0))

        # Check the moves for the Spider at (-3, -1) after moving the grasshopper
        original_expected_possible_moves = {(-4, -4), (-4, 1), (-2, -3), (-2, 2)}
        added_expected_possible_moves = {(-2, 1), (-2, -2), (-1, 1), (-1, -1), (-1, -2), (-1, 2)}
        spiders_location = {(-3, -1)}
        all_expected_possible_moves = original_expected_possible_moves.union(
            added_expected_possible_moves,
            spiders_location
        )
        actual_possible_moves = board.HiveGameBoard().pieces[(-3, -1)].possible_moves

        self.assertEqual(all_expected_possible_moves, actual_possible_moves)


if __name__ == '__main__':
    unittest.main()
