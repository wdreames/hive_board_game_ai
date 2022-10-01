import unittest
import src.game.board as board


class TestAntNoMovement(unittest.TestCase):

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

        game_board.print_board()

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


class TestAntWithMovement(unittest.TestCase):

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


class TestAntWithMovement3(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
