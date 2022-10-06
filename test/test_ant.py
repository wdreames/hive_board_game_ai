import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestAntBoard1Move0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ant_board1()
        board.HiveGameBoard().print_board()

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2), (1, -1), (2, -1)})
        expected_possible_moves.remove((1, 1))
        actual_possible_moves = board.HiveGameBoard().pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-1, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = board.HiveGameBoard().pieces[(-1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2), (1, -1), (2, -1)})
        expected_possible_moves.remove((-2, 1))
        actual_possible_moves = board.HiveGameBoard().pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (-2, -3)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        expected_possible_moves.remove((-2, -4))
        actual_possible_moves = board.HiveGameBoard().pieces[(-2, -3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant5(self):
        # Test ant movement at (0, -1)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(2, -1)})
        actual_possible_moves = board.HiveGameBoard().pieces[(0, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant6(self):
        # Test ant movement at (1, -2)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2)})
        actual_possible_moves = board.HiveGameBoard().pieces[(1, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant7(self):
        # Test ant movement at (2, -2)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2), (1, -1), (2, -1)})
        expected_possible_moves.remove((2, -3))
        actual_possible_moves = board.HiveGameBoard().pieces[(2, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant8(self):
        # Test ant movement at (2, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2)})
        expected_possible_moves.remove((2, 1))
        actual_possible_moves = board.HiveGameBoard().pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard1Move1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ant_board1()
        game_board = board.HiveGameBoard()
        game_board.move_piece((-2, -3), (1, 0))
        game_board.print_board()

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = board.HiveGameBoard().pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-1, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = board.HiveGameBoard().pieces[(-1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        expected_possible_moves.remove((-2, 1))
        actual_possible_moves = board.HiveGameBoard().pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (1, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = board.HiveGameBoard().pieces[(1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant5(self):
        # Test ant movement at (0, -1)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = board.HiveGameBoard().pieces[(0, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant6(self):
        # Test ant movement at (1, -2)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys())
        actual_possible_moves = board.HiveGameBoard().pieces[(1, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant7(self):
        # Test ant movement at (2, -2)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        expected_possible_moves.remove((2, -3))
        actual_possible_moves = board.HiveGameBoard().pieces[(2, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant8(self):
        # Test ant movement at (2, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys())
        actual_possible_moves = board.HiveGameBoard().pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard1Move2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ant_board1()
        game_board = board.HiveGameBoard()
        game_board.move_piece((-2, -3), (1, 0))
        game_board.move_piece((2, 0), (-1, -2))
        game_board.print_board()

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        actual_possible_moves = board.HiveGameBoard().pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-1, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys())
        actual_possible_moves = board.HiveGameBoard().pieces[(-1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        expected_possible_moves.remove((-2, 1))
        actual_possible_moves = board.HiveGameBoard().pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (1, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        expected_possible_moves.remove((2, 1))
        actual_possible_moves = board.HiveGameBoard().pieces[(1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant5(self):
        # Test ant movement at (0, -1)
        expected_possible_moves = set()
        actual_possible_moves = board.HiveGameBoard().pieces[(0, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant6(self):
        # Test ant movement at (1, -2)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        actual_possible_moves = board.HiveGameBoard().pieces[(1, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant7(self):
        # Test ant movement at (2, -2)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        expected_possible_moves.remove((2, -3))
        actual_possible_moves = board.HiveGameBoard().pieces[(2, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant8(self):
        # Test ant movement at (-1, -2)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys())
        actual_possible_moves = board.HiveGameBoard().pieces[(-1, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard2Move0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ant_board2()
        board.HiveGameBoard().print_board()

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, 0), (-2, -1), (-2, -2), (-3, -2)})
        actual_possible_moves = board.HiveGameBoard().pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys())
        actual_possible_moves = board.HiveGameBoard().pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-4, -2)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, 0)}, {(-5, -2), (-5, -3)})
        actual_possible_moves = board.HiveGameBoard().pieces[(-4, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (-3, -3)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-1, 0)}, {(-4, -4)})
        actual_possible_moves = board.HiveGameBoard().pieces[(-3, -3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard2Move1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ant_board2()
        board.HiveGameBoard().place_piece(spaces.Piece.BEETLE, (0, 2))  # Black

        # Combine prevention sets in the middle of the group
        board.HiveGameBoard().move_piece((-1, -1), (1, 1))  # White

        board.HiveGameBoard().print_board()

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = {(-1, 0), (-2, -1), (-2, -2), (-3, -2), (-1, -1)}
        actual_possible_moves = board.HiveGameBoard().pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys())
        actual_possible_moves = board.HiveGameBoard().pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-4, -2)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-5, -2), (-5, -3)})
        actual_possible_moves = board.HiveGameBoard().pieces[(-4, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (-3, -3)
        expected_possible_moves = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-4, -4)})
        actual_possible_moves = board.HiveGameBoard().pieces[(-3, -3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


def ant_board1():
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
    game_board.place_piece('Ant', (0, 0))  # White
    game_board.place_piece('Ant', (0, -1))  # Black
    game_board.place_piece('Ant', (-1, 0))  # White
    game_board.place_piece('Queen Bee', (0, -2))  # Black
    game_board.place_piece('Ant', (-2, 0))  # White
    game_board.place_piece('Ant', (1, -2))  # Black

    game_board.place_piece('Queen Bee', (-3, -1))  # White
    game_board.place_piece('Ant', (2, -2))  # Black
    game_board.place_piece('Grasshopper', (-3, -2))  # White
    game_board.place_piece('Grasshopper', (3, -1))  # Black
    game_board.place_piece('Grasshopper', (-3, -3))  # White
    game_board.place_piece('Grasshopper', (3, 0))  # Black
    game_board.place_piece('Ant', (-2, -3))  # White

    game_board.place_piece('Ant', (2, 0))  # Black


def ant_board2():
    game_board = board.HiveGameBoard(new_board=True)
    ant = spaces.Piece.ANT
    beetle = spaces.Piece.BEETLE
    grasshopper = spaces.Piece.GRASSHOPPER
    queen_bee = spaces.Piece.QUEEN_BEE
    spider = spaces.Piece.SPIDER

    game_board.place_piece(ant, (0, 0))  # White
    game_board.place_piece(queen_bee, (0, 1))  # Black
    game_board.place_piece(grasshopper, (-1, -1))  # White
    game_board.place_piece(spider, (-1, 1))  # Black
    game_board.place_piece(queen_bee, (0, -1))  # White
    game_board.place_piece(ant, (-2, 0))  # Black
    game_board.place_piece(grasshopper, (-1, -2))  # White
    game_board.place_piece(spider, (-3, -1))  # Black
    game_board.place_piece(spider, (-2, -3))  # White
    game_board.place_piece(ant, (-4, -2))  # Black
    game_board.place_piece(ant, (-3, -3))  # White



if __name__ == '__main__':
    unittest.main()
