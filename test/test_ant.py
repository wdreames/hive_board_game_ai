import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestAntBoard1Move0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = ant_board1()
        cls.game_board.print_board()

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2), (1, -1), (2, -1)})
        expected_possible_moves.remove((1, 1))
        actual_possible_moves = self.game_board.pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-1, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = self.game_board.pieces[(-1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2), (1, -1), (2, -1)})
        expected_possible_moves.remove((-2, 1))
        actual_possible_moves = self.game_board.pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (-2, -3)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        expected_possible_moves.remove((-2, -4))
        actual_possible_moves = self.game_board.pieces[(-2, -3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant5(self):
        # Test ant movement at (0, -1)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(2, -1)})
        actual_possible_moves = self.game_board.pieces[(0, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant6(self):
        # Test ant movement at (1, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2)})
        actual_possible_moves = self.game_board.pieces[(1, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant7(self):
        # Test ant movement at (2, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2), (1, -1), (2, -1)})
        expected_possible_moves.remove((2, -3))
        actual_possible_moves = self.game_board.pieces[(2, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant8(self):
        # Test ant movement at (2, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2), (-1, -2)})
        expected_possible_moves.remove((2, 1))
        actual_possible_moves = self.game_board.pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard1Move1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = ant_board1()
        cls.game_board.move_piece((-2, -3), (1, 0))
        cls.game_board.print_board()

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = self.game_board.pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-1, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = self.game_board.pieces[(-1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        expected_possible_moves.remove((-2, 1))
        actual_possible_moves = self.game_board.pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (1, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = self.game_board.pieces[(1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant5(self):
        # Test ant movement at (0, -1)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        actual_possible_moves = self.game_board.pieces[(0, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant6(self):
        # Test ant movement at (1, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys())
        actual_possible_moves = self.game_board.pieces[(1, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant7(self):
        # Test ant movement at (2, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(1, -1), (2, -1)})
        expected_possible_moves.remove((2, -3))
        actual_possible_moves = self.game_board.pieces[(2, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant8(self):
        # Test ant movement at (2, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys())
        actual_possible_moves = self.game_board.pieces[(2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard1Move2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = ant_board1()
        cls.game_board.move_piece((-2, -3), (1, 0))
        cls.game_board.move_piece((2, 0), (-1, -2))
        cls.game_board.print_board()

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        actual_possible_moves = self.game_board.pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-1, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys())
        actual_possible_moves = self.game_board.pieces[(-1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        expected_possible_moves.remove((-2, 1))
        actual_possible_moves = self.game_board.pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (1, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        expected_possible_moves.remove((2, 1))
        actual_possible_moves = self.game_board.pieces[(1, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant5(self):
        # Test ant movement at (0, -1)
        expected_possible_moves = set()
        actual_possible_moves = self.game_board.pieces[(0, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant6(self):
        # Test ant movement at (1, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        actual_possible_moves = self.game_board.pieces[(1, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant7(self):
        # Test ant movement at (2, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, -1), (-2, -1), (-2, -2)})
        expected_possible_moves.remove((2, -3))
        actual_possible_moves = self.game_board.pieces[(2, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant8(self):
        # Test ant movement at (-1, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys())
        actual_possible_moves = self.game_board.pieces[(-1, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard2Move0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = ant_board2()
        cls.game_board.print_board()

    def test_prevention_sets(self):
        expected_prevention_sets = [{(-1, 0)}, {(-2, -1), (-2, -2), (-3, -2)}]
        actual_prevention_sets = self.game_board.ant_mvt_prevention_sets
        self.assertEqual(expected_prevention_sets, actual_prevention_sets)

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, 0), (-2, -1), (-2, -2), (-3, -2)})
        actual_possible_moves = self.game_board.pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys())
        actual_possible_moves = self.game_board.pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-4, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, 0)}, {(-5, -2), (-5, -3)})
        actual_possible_moves = self.game_board.pieces[(-4, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (-3, -3)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, 0)}, {(-4, -4)})
        actual_possible_moves = self.game_board.pieces[(-3, -3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard2Move1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = ant_board2()
        cls.game_board.place_piece(spaces.Piece.BEETLE, (0, 2))  # Black

        # Combine prevention sets in the middle of the group
        cls.game_board.move_piece((-1, -1), (1, 1))  # White

        cls.game_board.print_board()

    def test_prevention_sets(self):
        expected_prevention_sets = [{(-1, 0), (-1, -1), (-2, -1), (-2, -2), (-3, -2)}]
        actual_prevention_sets = self.game_board.ant_mvt_prevention_sets
        self.assertEqual(expected_prevention_sets, actual_prevention_sets)

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = {(-1, 0), (-2, -1), (-2, -2), (-3, -2), (-1, -1)}
        actual_possible_moves = self.game_board.pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys())
        actual_possible_moves = self.game_board.pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-4, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-5, -2), (-5, -3)})
        actual_possible_moves = self.game_board.pieces[(-4, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (-3, -3)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-4, -4)})
        actual_possible_moves = self.game_board.pieces[(-3, -3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard2Move2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = ant_board2()
        cls.game_board.place_piece(spaces.Piece.BEETLE, (0, 2))  # Black

        # Combine prevention sets in the middle of the group
        cls.game_board.move_piece((-1, -1), (1, 1))  # White

        # Filler move for black
        cls.game_board.move_piece((0, 2), (-1, 2))  # Black

        # Separate prevention sets again
        cls.game_board.move_piece((1, 1), (-1, -1))

        cls.game_board.print_board()

    def test_prevention_sets(self):
        expected_prevention_sets = [{(-1, 0)}, {(-2, -1), (-2, -2), (-3, -2)}]
        actual_prevention_sets = self.game_board.ant_mvt_prevention_sets
        self.assertEqual(expected_prevention_sets, actual_prevention_sets)

    def test_ant1(self):
        # Test ant movement at (0, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, 0), (-2, -1), (-2, -2), (-3, -2)})
        actual_possible_moves = self.game_board.pieces[(0, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant2(self):
        # Test ant movement at (-2, 0)
        expected_possible_moves = set(self.game_board.empty_spaces.keys())
        actual_possible_moves = self.game_board.pieces[(-2, 0)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant3(self):
        # Test ant movement at (-4, -2)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, 0)}, {(-5, -2), (-5, -3)})
        actual_possible_moves = self.game_board.pieces[(-4, -2)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_ant4(self):
        # Test ant movement at (-3, -3)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference(
            {(-1, 0)}, {(-4, -4)})
        actual_possible_moves = self.game_board.pieces[(-3, -3)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntBoard3(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(beetle, (0, 0))
        game_board.place_piece(queen_bee, (0, 1))
        game_board.place_piece(queen_bee, (0, -1))
        game_board.place_piece(spider, (0, 2))
        game_board.place_piece(beetle, (-1, -1))
        game_board.move_piece((0, 2), (1, 0))
        game_board.move_piece((-1, -1), (-1, 0))
        game_board.place_piece(ant, (1, 2))
        game_board.place_piece(ant, (-1, -1))
        game_board.place_piece(ant, (2, 2))
        game_board.move_piece((0, 0), (0, 1))

        game_board.print_board()

        cls.game_board = game_board

    def test_ant(self):
        # Test ant movement at (-1, -1)
        expected_possible_moves = set(self.game_board.empty_spaces.keys()).difference({
            (0, 0),  # New prevention set made by beetle moving out of the middle of a group of pieces
            (1, 1),  # Blocked by sliding rules
            (-2, -2)  # Only connected to Ant
        })
        actual_possible_moves = self.game_board.pieces[(-1, -1)].possible_moves

        self.assertEqual(expected_possible_moves, actual_possible_moves)


class TestAntErrorsFromRandomBoards(unittest.TestCase):
    """
    This class tests errors found from running random games.
    The test cases pass if no errors occur.
    """

    @staticmethod
    def _test_game_helper(actions):
        game_board = board.BoardManager(new_manager=True)
        for action in actions[:-3]:
            game_board.perform_action(action)
        game_board.get_board().print_board()

        for action in actions[-3:-1]:
            game_board.perform_action(action)
            game_board.get_board().print_board()

        print(game_board.get_board())

        print(f'Perfoming final action: {actions[-1]}:')
        game_board.perform_action(actions[-1])
        game_board.get_board().print_board()

    def test_game_one(self):
        actions = [
            ('Place Piece', (0, 0), 'Grasshopper'),
            ('Place Piece', (1, 1), 'Spider'),
            ('Place Piece', (-1, -1), 'Queen Bee'),
            ('Place Piece', (2, 2), 'Beetle'),
            ('Place Piece', (-1, -2), 'Grasshopper'),
            ('Place Piece', (3, 2), 'Spider'),
            ('Place Piece', (-2, -1), 'Ant'),
            ('Place Piece', (4, 2), 'Queen Bee'),
            ('Place Piece', (-1, 0), 'Beetle'),
            ('Place Piece', (1, 2), 'Beetle'),
            ('Place Piece', (-2, -2), 'Ant'),
            ('Move Piece', (1, 2), (2, 3)),
            ('Move Piece', (-1, 0), (0, 0)),
            ('Place Piece', (4, 3), 'Ant'),
            ('Move Piece', (-2, -2), (-1, 0)),
            ('Move Piece', (4, 3), (-3, -1)),
            ('Move Piece', (-1, 0), (-3, 0)),
            ('Move Piece', (2, 3), (3, 3)),
            ('Move Piece', (-3, 0), (-1, -3)),
            ('Move Piece', (-3, -1), (-2, -2)),
            ('Place Piece', (-2, -4), 'Beetle'),
            ('Place Piece', (1, 2), 'Grasshopper'),
            ('Move Piece', (-2, -1), (1, 3)),
            ('Move Piece', (-2, -2), (-1, 0)),
            ('Move Piece', (-2, -4), (-1, -4)),
            ('Move Piece', (-1, 0), (4, 1)),
            ('Move Piece', (0, 0), (-1, -1)),
            ('Move Piece', (4, 1), (3, 1)),
            ('Move Piece', (1, 3), (3, 0)),
            ('Place Piece', (5, 3), 'Grasshopper'),
            ('Move Piece', (-1, -4), (-1, -3)),
            ('Place Piece', (4, 4), 'Ant'),
            ('Move Piece', (3, 0), (1, 0)),
            ('Move Piece', (3, 1), (0, -2)),
            ('Place Piece', (-1, 0), 'Ant'),
            ('Place Piece', (6, 4), 'Ant'),
            ('Place Piece', (-2, -3), 'Spider'),
            ('Place Piece', (3, 4), 'Grasshopper'),
            ('Move Piece', (1, 0), (-2, 0)),
            ('Move Piece', (0, -2), (5, 5)),
            ('Move Piece', (-2, 0), (-1, -4)),
            ('Move Piece', (6, 4), (3, 5)),
            ('Place Piece', (-3, -3), 'Spider'),
            ('Move Piece', (5, 5), (0, -4)),
            ('Move Piece', (-1, -1), (-1, 0)),
            ('Move Piece', (4, 4), (1, -4)),
            ('Move Piece', (-1, -3), (0, -3)),
            ('Move Piece', (1, -4), (-3, -4)),
            ('Move Piece', (-1, -4), (1, -4)),
            ('Move Piece', (-3, -4), (5, 4)),
            ('Place Piece', (0, -2), 'Grasshopper'),
            ('Move Piece', (5, 4), (2, 3)),
            ('Move Piece', (-1, 0), (-1, -1)),
            ('Move Piece', (3, 5), (0, -1)),
            ('Move Piece', (1, -4), (0, 1)),
            ('Move Piece', (2, 3), (4, 4)),
            ('Move Piece', (0, 1), (2, 1)),
            ('Move Piece', (4, 4), (-1, -4)),
            ('Move Piece', (-1, 0), (1, -4)),
            ('Move Piece', (0, -1), (4, 3)),
            ('Move Piece', (0, -3), (-1, -3)),
            ('Move Piece', (4, 3), (2, 0)),
            ('Move Piece', (-1, -1), (-1, -2)),
            ('Move Piece', (2, 0), (5, 2)),
            ('Move Piece', (-1, -3), (-2, -3)),
            ('Move Piece', (5, 2), (0, -1)),
            ('Move Piece', (1, -4), (3, 5)),
            ('Move Piece', (0, -4), (-2, -1)),
            ('Move Piece', (2, 1), (-3, -4)),
            ('Move Piece', (-1, -4), (1, -1)),
            ('Move Piece', (3, 5), (3, 1)),
            ('Move Piece', (1, -1), (5, 4)),
            ('Move Piece', (3, 1), (4, 1)),
            ('Move Piece', (5, 4), (-3, -1)),
            ('Move Piece', (4, 1), (1, 3)),
            ('Move Piece', (0, -1), (4, 5)),
            ('Move Piece', (-3, -4), (0, 3)),
            ('Move Piece', (4, 5), (-1, 2)),
            ('Move Piece', (-2, -3), (-3, -3)),
            ('Move Piece', (-3, -1), (0, 4)),
            ('Move Piece', (-1, -3), (-2, -4)),
            ('Move Piece', (-2, -1), (-3, -2)),
            ('Move Piece', (-2, -4), (6, 3)),
            ('Move Piece', (-1, 2), (-2, -1)),
            ('Move Piece', (-2, -3), (-4, -3)),
            ('Move Piece', (0, 4), (6, 2)),
            ('Move Piece', (-3, -3), (-3, -4)),
            ('Move Piece', (6, 2), (-5, -4)),
            ('Move Piece', (0, 3), (-3, -1)),
            ('Move Piece', (-5, -4), (7, 4)),
            ('Move Piece', (-1, -2), (-2, -2)),
            ('Move Piece', (7, 4), (0, 3)),
            ('Move Piece', (-3, -1), (6, 4)),
            ('Move Piece', (-3, -2), (-2, 0)),
            ('Move Piece', (6, 4), (0, -3)),
            ('Move Piece', (0, 3), (-2, -4)),
            ('Move Piece', (1, 3), (4, 5)),
            ('Move Piece', (-2, -4), (6, 2)),
            ('Move Piece', (0, -3), (-1, -3)),
            ('Move Piece', (6, 2), (6, 4)),
            ('Move Piece', (-1, -3), (6, 2)),
            ('Move Piece', (6, 4), (3, 5)),
            ('Move Piece', (4, 5), (7, 3)),
            ('Move Piece', (-2, 0), (-5, -4)),
            ('Move Piece', (7, 3), (-4, -4)),
            ('Move Piece', (-5, -4), (6, 4)),
            ('Move Piece', (6, 2), (4, 1)),
            ('Move Piece', (-2, -1), (2, 3)),
            ('Move Piece', (4, 1), (-2, -4)),
            ('Move Piece', (6, 4), (-4, -2)),
            ('Move Piece', (-2, -4), (3, 6)),
            ('Move Piece', (-4, -2), (5, 2)),
            ('Move Piece', (3, 6), (-5, -3)),
            ('Move Piece', (3, 5), (-1, -3)),
            ('Move Piece', (6, 3), (-3, -2)),
            ('Move Piece', (2, 3), (1, 3)),
            ('Move Piece', (-4, -4), (4, 3)),
            ('Move Piece', (1, 3), (5, 4)),
            ('Move Piece', (-5, -3), (0, 2)),
            ('Move Piece', (-1, -3), (6, 3)),
            ('Move Piece', (-3, -2), (-2, -1)),
            ('Move Piece', (6, 3), (-1, 0)),
            ('Move Piece', (0, 2), (-2, -3)),
            ('Move Piece', (-1, 0), (-4, -2)),
            ('Move Piece', (-2, -1), (5, 1)),
            ('Move Piece', (-4, -2), (2, 1)),
            ('Move Piece', (-2, -3), (6, 5)),
            ('Move Piece', (2, 2), (3, 2)),
            ('Move Piece', (6, 5), (-4, -4)),
            ('Move Piece', (5, 3), (2, 3)),
            ('Move Piece', (5, 1), (1, 0)),
            ('Move Piece', (3, 2), (3, 1)),
            ('Move Piece', (1, 0), (3, 0)),
            ('Move Piece', (5, 4), (-5, -5)),
            ('Move Piece', (3, 0), (-4, -2)),
            ('Move Piece', (5, 2), (-2, -4)),
            ('Move Piece', (-4, -2), (1, 0)),
            ('Move Piece', (-2, -4), (3, 5)),
            ('Move Piece', (4, 3), (4, 1)),
            ('Move Piece', (3, 5), (1, -1)),
            ('Move Piece', (4, 1), (1, 3)),
            ('Move Piece', (3, 4), (0, 1)),
            ('Move Piece', (-3, -4), (-4, -4)),
            ('Move Piece', (1, -1), (1, 4)),
            ('Move Piece', (1, 0), (1, -1)),
            ('Move Piece', (-5, -5), (5, 2)),
            ('Move Piece', (1, -1), (-1, 0)),
            ('Move Piece', (5, 2), (-5, -3)),
            ('Move Piece', (-1, 0), (2, 4)),
            ('Move Piece', (2, 1), (1, -1)),
            ('Move Piece', (1, 3), (-1, 1)),
            ('Move Piece', (-5, -3), (-2, -1)),
            ('Move Piece', (-1, 1), (0, 2)),
            ('Move Piece', (-2, -1), (2, 5)),
            ('Move Piece', (-4, -4), (-3, -3)),
            ('Move Piece', (2, 5), (-2, -1)),
            ('Move Piece', (-3, -3), (-2, -2)),
            ('Move Piece', (-2, -1), (3, 5)),
            ('Move Piece', (-2, -2), (-2, -3)),
            ('Move Piece', (3, 5), (1, 0)),
            ('Move Piece', (0, 2), (0, -3)),
            ('Move Piece', (1, 0), (3, 4)),
            ('Move Piece', (-4, -4), (-4, -2)),
            ('Move Piece', (3, 4), (-3, -1)),
            ('Move Piece', (0, -3), (-2, -1)),
            ('Move Piece', (1, 4), (-3, -4)),
            ('Move Piece', (2, 4), (-4, -4)),
            ('Move Piece', (1, -1), (5, 2)),
            ('Move Piece', (-4, -2), (4, 1)),
            ('Move Piece', (-3, -1), (4, 3)),
            ('Move Piece', (4, 1), (2, 1)),
            ('Move Piece', (3, 3), (3, 2)),
            ('Move Piece', (-2, -1), (1, 3)),
            ('Move Piece', (5, 2), (0, -3)),
            ('Move Piece', (1, 3), (1, 0)),
            ('Move Piece', (-3, -4), (3, 4)),
            ('Move Piece', (1, 0), (0, -1)),
            ('Move Piece', (4, 3), (2, 4)),
            ('Move Piece', (-4, -4), (4, 1)),
            ('Move Piece', (3, 4), (3, 0)),
            ('Move Piece', (0, -1), (-1, 0)),
            ('Move Piece', (3, 1), (4, 1)),
            ('Move Piece', (-1, 0), (5, 1)),
            ('Move Piece', (3, 0), (1, 4)),
            ('Move Piece', (5, 1), (0, 3)),
            ('Move Piece', (3, 2), (4, 3)),
            ('Move Piece', (0, 3), (1, -2)),
            ('Move Piece', (0, -3), (0, 3)),
            ('Move Piece', (1, -2), (0, 2)),
            ('Move Piece', (1, 4), (5, 4)),
            ('Move Piece', (-2, -3), (-1, -2)),
            ('Move Piece', (2, 4), (3, 1)),
            ('Move Piece', (0, -2), (-3, -2)),
            ('Move Piece', (3, 1), (6, 4)),
            ('Move Piece', (-1, -2), (-1, -1)),
            ('Move Piece', (6, 4), (-4, -2)),
            ('Move Piece', (-1, -1), (-2, -1)),
            ('Move Piece', (-4, -2), (3, 0)),
            ('Move Piece', (-3, -3), (-5, -3)),
            ('Move Piece', (5, 4), (-4, -2)),
            ('Move Piece', (-2, -2), (-2, -3)),
            ('Move Piece', (-4, -2), (3, 3)),
            ('Move Piece', (2, 1), (-1, 2)),
            ('Move Piece', (3, 0), (5, 2)),
            ('Move Piece', (-1, 2), (-2, -4)),
            ('Move Piece', (0, 3), (-4, -2)),
            ('Move Piece', (-2, -4), (-1, -3)),
            ('Move Piece', (5, 2), (2, 4)),
            ('Move Piece', (-5, -3), (-3, -3)),
            ('Move Piece', (4, 1), (5, 1)),
            ('Move Piece', (0, 2), (4, 0)),
            ('Move Piece', (-4, -2), (3, 1)),
            ('Move Piece', (4, 0), (6, 1)),
            ('Move Piece', (3, 2), (2, 0)),
            ('Move Piece', (-1, -2), (-1, 0)),
            ('Move Piece', (2, 4), (4, 0)),
            ('Move Piece', (-1, -3), (6, 2)),
            ('Move Piece', (4, 0), (5, 2)),
            ('Move Piece', (0, 0), (2, 2)),
            ('Move Piece', (5, 2), (-2, 0)),
            ('Move Piece', (6, 1), (-1, 1)),
            ('Move Piece', (-2, 0), (-4, -2)),
            ('Move Piece', (-1, 1), (7, 2)),
            ('Move Piece', (-4, -2), (8, 3)),
            ('Move Piece', (-1, -1), (-2, -2)),
            ('Move Piece', (8, 3), (3, 4)),
            ('Move Piece', (7, 2), (-1, -3)),
            ('Move Piece', (1, 2), (4, 5)),
            ('Move Piece', (6, 2), (-5, -4)),
            ('Move Piece', (2, 3), (2, 1)),
            ('Move Piece', (-5, -4), (0, 2)),
            ('Move Piece', (4, 3), (4, 4)),
            ('Move Piece', (-3, -3), (-1, -4)),
            ('Move Piece', (3, 4), (1, 0)),
            ('Move Piece', (0, 2), (0, -2)),
            ('Move Piece', (1, 0), (-4, -4)),
            ('Move Piece', (0, -2), (6, 1)),
            ('Move Piece', (-4, -4), (4, 3)),
            ('Move Piece', (2, 2), (2, -1)),
            ('Move Piece', (3, 3), (5, 5)),
            ('Move Piece', (6, 1), (6, 5)),
            ('Move Piece', (4, 5), (4, 0)),
            ('Move Piece', (6, 5), (-3, -3)),
            ('Move Piece', (5, 5), (2, 2)),
            ('Move Piece', (-3, -3), (-5, -3)),
            ('Move Piece', (2, 2), (6, 2)),
            ('Move Piece', (-5, -3), (6, 3)),
            ('Move Piece', (4, 4), (3, 3)),
            ('Move Piece', (6, 3), (7, 3)),
            ('Move Piece', (4, 0), (8, 4)),
            ('Move Piece', (-4, -3), (-2, -4)),
            ('Move Piece', (8, 4), (4, 0)),
            ('Move Piece', (7, 3), (2, 2)),
            ('Move Piece', (4, 3), (-1, -1)),
            ('Move Piece', (-1, -3), (0, -1)),
            ('Move Piece', (6, 2), (6, 1)),
            ('Move Piece', (0, -1), (1, 2)),
            ('Move Piece', (6, 1), (3, -1)),
            ('Move Piece', (1, 2), (-3, -5)),
            ('Move Piece', (3, -1), (1, 2)),
            ('Move Piece', (-3, -5), (-1, 1)),
            ('Move Piece', (1, 2), (0, -1)),
            ('Move Piece', (-3, -2), (1, 2)),
            ('Move Piece', (0, -1), (0, -3)),
            ('Move Piece', (-1, 1), (0, -2)),
            ('Move Piece', (-1, -1), (1, -1)),
            ('Move Piece', (0, -2), (1, -1)),
        ]
        self.assertRaisesRegex(
            RuntimeError,
            "[Illegal action. Piece at ] [cannot move to]",
            self._test_game_helper,
            actions
        )


def ant_board1():
    game_board = board.HiveGameBoard()

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

    return game_board


def ant_board2():
    game_board = board.HiveGameBoard()
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

    return game_board


if __name__ == '__main__':
    unittest.main()
