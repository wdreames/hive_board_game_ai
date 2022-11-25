import os
import pickle
import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestSpiderBoard1Move0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(spider, (0, 0))  # White
        game_board.place_piece(queen_bee, (0, 1))  # Black

        game_board.print_board()

        cls.game_board = game_board

    def test_spider1(self):
        # Test Spider at (0, 0)
        expected_possible_moves = {(0, 2)}
        actual_possible_moves = self.game_board.pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard1Move1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard()
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

        cls.game_board = game_board

    def test_spider1(self):
        # Test Spider at (0, 0)
        expected_possible_moves = {(0, -2), (-1, 2), (1, 3)}
        actual_possible_moves = self.game_board.pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard1Move2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard()
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

        cls.game_board = game_board

    def test_spider1(self):
        # Test Spider at (0, 0)
        expected_possible_moves = {(0, 2), (-1, -3)}
        actual_possible_moves = self.game_board.pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderMoveOntoSelf(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard()
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

        cls.game_board = game_board

    def test_spider1(self):
        # Test Spider at (-1, 1)
        expected_possible_moves = {(-1, 1), (-1, -1), (-1, 3)}
        actual_possible_moves = self.game_board.pieces[(-1, 1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

        # Move onto itself
        self.game_board.move_piece((-1, 1), (-1, 1))
        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test Spider at (1, 3)
        expected_possible_moves = {(-1, 3), (2, 1)}
        actual_possible_moves = self.game_board.pieces[(1, 3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard2Move0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(queen_bee, (0, 0))
        game_board.place_piece(queen_bee, (1, 0))
        game_board.place_piece(spider, (-1, -1))
        game_board.place_piece(spider, (2, 0))

        game_board.print_board()

        cls.game_board = game_board

    def test_spider1(self):
        # Test spider at (-1, -1)
        expected_possible_moves = {(2, -1), (1, 1)}
        actual_possible_moves = self.game_board.pieces[(-1, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test spider at (2, 0)
        expected_possible_moves = {(-1, -2), (0, 1)}
        actual_possible_moves = self.game_board.pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard2Move1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(queen_bee, (0, 0))
        game_board.place_piece(queen_bee, (1, 0))
        game_board.place_piece(spider, (-1, -1))
        game_board.place_piece(spider, (2, 0))

        game_board.move_piece((-1, -1), (2, -1))

        game_board.print_board()

        cls.game_board = game_board

    def test_spider1(self):
        # Test spider at (2, -1)
        expected_possible_moves = {(-1, -1), (2, 1)}
        actual_possible_moves = self.game_board.pieces[(2, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test spider at (2, 0)
        expected_possible_moves = {(2, -2), (0, 1)}
        actual_possible_moves = self.game_board.pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard2Move2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(queen_bee, (0, 0))
        game_board.place_piece(queen_bee, (1, 0))
        game_board.place_piece(spider, (-1, -1))
        game_board.place_piece(spider, (2, 0))

        game_board.move_piece((-1, -1), (2, -1))

        game_board.place_piece(grasshopper, (3, 1))
        game_board.place_piece(beetle, (-1, 0))

        game_board.print_board()

        cls.game_board = game_board

    def test_spider1(self):
        # Test spider at (2, -1)
        expected_possible_moves = {(-1, -1), (4, 2)}
        actual_possible_moves = self.game_board.pieces[(2, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test spider at (2, 0)
        expected_possible_moves = set()
        actual_possible_moves = self.game_board.pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard2Move3(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(queen_bee, (0, 0))
        game_board.place_piece(queen_bee, (1, 0))
        game_board.place_piece(spider, (-1, -1))
        game_board.place_piece(spider, (2, 0))

        game_board.move_piece((-1, -1), (2, -1))

        game_board.place_piece(grasshopper, (3, 1))
        game_board.place_piece(beetle, (-1, 0))

        game_board.move_piece((3, 1), (1, -1))

        game_board.print_board()

        cls.game_board = game_board

    def test_spider1(self):
        # Test spider at (2, -1)
        expected_possible_moves = {(0, -1), (2, 1)}
        actual_possible_moves = self.game_board.pieces[(2, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider2(self):
        # Test spider at (2, 0)
        expected_possible_moves = {(2, -2), (0, 1)}
        actual_possible_moves = self.game_board.pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestSpiderBoard3(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manager = board.BoardManager(new_manager=True)
        with open(os.path.join('test', 'data', 'spider_board_3.hv'), 'rb') as file:
            game_state = pickle.load(file)
            cls.manager.current_board = game_state

    # Ensure that the following does not cause an error
    def test_spider1(self):
        # The pickle of this object was made before this attribute was added. Adding it here.
        self.manager.current_board.disconnected_empty_spaces = set()

        self.manager.perform_action((board.HiveGameBoard.PLACE_PIECE, (3, 2), spaces.Piece.GRASSHOPPER))
        self.manager.perform_action((board.HiveGameBoard.MOVE_PIECE, (-3, -2), (0, -1)))
        self.manager.perform_action((board.HiveGameBoard.MOVE_PIECE, (0, 2), (1, -2)))

        self.manager.get_successor(('Move Piece', (0, 1), (0, -2)))
        self.manager.get_predecessor()

        self.manager.perform_action((board.HiveGameBoard.MOVE_PIECE, (0, -1), (0, -2)))


class TestSpiderOverlappingPaths(unittest.TestCase):

    @staticmethod
    def setup_spider_test_board():
        game_board = board.HiveGameBoard()
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

        return game_board

    def test_spider_before_move(self):
        game_board = self.setup_spider_test_board()
        # Test Spider at (-4, -4) before moving
        expected_possible_moves = {(-3, -1), (-2, -5)}
        actual_possible_moves = game_board.pieces[(-4, -4)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider_after_move(self):
        game_board = self.setup_spider_test_board()
        game_board.move_piece((-4, -4), (-3, -1))

        # Check the moves for the Spider after moving to (-3, -1)
        expected_possible_moves = {(-4, -4), (-4, 1), (-2, -3), (-2, 2)}
        actual_possible_moves = game_board.pieces[(-3, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_spider_moves_updated(self):
        game_board = self.setup_spider_test_board()
        game_board.move_piece((-4, -4), (-3, -1))

        # Move the grasshopper from (1, 2) to (-1, 0). This should update the Spiders set of possible moves.
        game_board.move_piece((1, 2), (-1, 0))

        # Check the moves for the Spider at (-3, -1) after moving the grasshopper
        original_expected_possible_moves = {(-4, -4), (-4, 1), (-2, -3), (-2, 2)}
        added_expected_possible_moves = {(-2, 1), (-2, -2), (-1, 1), (-1, -1), (-1, -2), (-1, 2)}
        spiders_location = {(-3, -1)}
        all_expected_possible_moves = original_expected_possible_moves.union(
            added_expected_possible_moves,
            spiders_location
        )
        actual_possible_moves = game_board.pieces[(-3, -1)].possible_moves

        self.assertEqual(all_expected_possible_moves, actual_possible_moves)

    def test_spider_moves_updated2(self):
        game_board = self.setup_spider_test_board()
        game_board.move_piece((-4, -4), (-3, -1))
        game_board.move_piece((1, 2), (-1, 0))

        # Make a move for white
        game_board.place_piece(spaces.Piece.GRASSHOPPER, (-4, -3))

        # Move the grasshopper back out
        game_board.move_piece((-1, 0), (1, 0))

        # Check the moves for the Spider at (-3, -1) after moving the grasshopper
        expected_possible_moves = {(-5, -4), (-4, 1), (-2, -3), (-2, 2)}
        actual_possible_moves = game_board.pieces[(-3, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


if __name__ == '__main__':
    unittest.main()
