import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestOneHiveBoard1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        cls.game_board.place_piece(ant, (0, 0))
        cls.game_board.place_piece(spider, (1, 1))
        cls.game_board.place_piece(grasshopper, (0, -1))
        cls.game_board.place_piece(beetle, (2, 2))
        cls.game_board.place_piece(queen_bee, (0, -2))
        cls.game_board.place_piece(queen_bee, (2, 1))
        cls.game_board.place_piece(ant, (1, -1))
        cls.game_board.place_piece(grasshopper, (1, 2))
        cls.game_board.place_piece(ant, (-1, 0))

        cls.game_board.move_piece((1, 2), (1, 0))
        cls.game_board.move_piece((-1, 0), (2, 0))

        cls.game_board.print_board()

    def test_all_pieces_can_move(self):
        for piece in self.game_board.pieces.values():
            self.assertTrue(piece.can_move, f'{piece.name} at {piece.location} should be able to move.')

    def test_all_pieces_in_possible_moves(self):
        expected_movable_pieces = set(self.game_board.pieces.keys())

        white_movable_pieces = set(self.game_board.white_possible_moves.keys())
        black_movable_pieces = set(self.game_board.black_possible_moves.keys())
        actual_movable_pieces = white_movable_pieces.union(black_movable_pieces)

        self.assertEqual(expected_movable_pieces, actual_movable_pieces)


class TestOneHiveBoard2Move0(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = one_hive_board2()
        cls.game_board.print_board()

        cls.pieces_that_can_move = {(2, 0), (-2, -3)}

    def test_pieces_can_move(self):
        for piece in self.game_board.pieces.values():
            if piece.location in self.pieces_that_can_move:
                self.assertTrue(piece.can_move, f'{piece.name} at {piece.location} should be able to move.')
            else:
                self.assertTrue(not piece.can_move, f'{piece.name} at {piece.location} should not be able to move.')

    def test_pieces_in_possible_moves(self):
        expected_movable_pieces = self.pieces_that_can_move

        white_movable_pieces = set(self.game_board.white_possible_moves.keys())
        black_movable_pieces = set(self.game_board.black_possible_moves.keys())
        actual_movable_pieces = white_movable_pieces.union(black_movable_pieces)

        self.assertEqual(expected_movable_pieces, actual_movable_pieces)


class TestOneHiveBoard2Move1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = one_hive_board2()
        cls.game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (-3, 0), piece_type=spaces.Piece.ANT)
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (2, 0), new_location=(1, 0))
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (-3, 0), new_location=(-1, -3))
        cls.game_board.print_board()

        cls.pieces_that_cannot_move = {(0, -2), (1, -2), (2, -2), (3, -1)}

    def test_pieces_can_move(self):
        for piece in self.game_board.pieces.values():
            if piece.location in self.pieces_that_cannot_move:
                self.assertTrue(not piece.can_move, f'{piece.name} at {piece.location} should not be able to move.')
            else:
                self.assertTrue(piece.can_move, f'{piece.name} at {piece.location} should be able to move.')

    def test_pieces_in_possible_moves(self):
        expected_movable_pieces = set(self.game_board.pieces.keys()).difference(self.pieces_that_cannot_move)

        white_movable_pieces = set(self.game_board.white_possible_moves.keys())
        black_movable_pieces = set(self.game_board.black_possible_moves.keys())
        actual_movable_pieces = white_movable_pieces.union(black_movable_pieces)

        self.assertEqual(expected_movable_pieces, actual_movable_pieces)


class TestOneHiveBoard2Move2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = one_hive_board2()
        cls.game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (-3, 0), piece_type=spaces.Piece.ANT)
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (2, 0), new_location=(1, 0))
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (-3, 0), new_location=(-1, -3))
        cls.game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (2, 0), piece_type=spaces.Piece.ANT)
        cls.game_board.print_board()

    def test_all_pieces_can_move(self):
        for piece in self.game_board.pieces.values():
            self.assertTrue(piece.can_move, f'{piece.name} at {piece.location} should be able to move.')

    def test_all_pieces_in_possible_moves(self):
        expected_movable_pieces = set(self.game_board.pieces.keys())
        expected_movable_pieces.remove((0, -2))  # This Piece has no possible moves in this configuration

        white_movable_pieces = set(self.game_board.white_possible_moves.keys())
        black_movable_pieces = set(self.game_board.black_possible_moves.keys())
        actual_movable_pieces = white_movable_pieces.union(black_movable_pieces)

        self.assertEqual(expected_movable_pieces, actual_movable_pieces)


class TestOneHiveBoard2Move3(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = one_hive_board2()
        cls.game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (-3, 0), piece_type=spaces.Piece.ANT)
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (2, 0), new_location=(1, 0))
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (-3, 0), new_location=(-1, -3))
        cls.game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (2, 0), piece_type=spaces.Piece.ANT)
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (-1, -3), new_location=(4, 1))
        cls.game_board.print_board()

        cls.pieces_that_cannot_move = {(3, 0), (0, 0), (-1, 0), (-2, 0), (-3, -1), (-3, -2), (-3, -3)}

    def test_pieces_can_move(self):
        for piece in self.game_board.pieces.values():
            if piece.location in self.pieces_that_cannot_move:
                self.assertTrue(not piece.can_move, f'{piece.name} at {piece.location} should not be able to move.')
            else:
                self.assertTrue(piece.can_move, f'{piece.name} at {piece.location} should be able to move.')

    def test_pieces_in_possible_moves(self):
        expected_movable_pieces = set(self.game_board.pieces.keys()).difference(self.pieces_that_cannot_move)

        white_movable_pieces = set(self.game_board.white_possible_moves.keys())
        black_movable_pieces = set(self.game_board.black_possible_moves.keys())
        actual_movable_pieces = white_movable_pieces.union(black_movable_pieces)

        self.assertEqual(expected_movable_pieces, actual_movable_pieces)


class TestOneHiveBoard2Move4(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game_board = one_hive_board2()
        cls.game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (-3, 0), piece_type=spaces.Piece.ANT)
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (2, 0), new_location=(1, 0))
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (-3, 0), new_location=(-1, -3))
        cls.game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (2, 0), piece_type=spaces.Piece.ANT)
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (-1, -3), new_location=(4, 1))
        cls.game_board.print_board()
        cls.game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (3, -1), new_location=(3, 1))
        cls.game_board.print_board()

        cls.pieces_that_cannot_move = {(0, 0), (-1, 0), (-2, 0), (-3, -1), (-3, -2), (-3, -3), (-2, -1),
                                       (0, -1), (0, -2), (1, -2), (1, 0), (2, 0)}

    def test_pieces_can_move(self):
        for piece in self.game_board.pieces.values():
            if piece.location in self.pieces_that_cannot_move:
                self.assertTrue(not piece.can_move, f'{piece.name} at {piece.location} should not be able to move.')
            else:
                self.assertTrue(piece.can_move, f'{piece.name} at {piece.location} should be able to move.')

    def test_pieces_in_possible_moves(self):
        expected_movable_pieces = set(self.game_board.pieces.keys()).difference(self.pieces_that_cannot_move)

        white_movable_pieces = set(self.game_board.white_possible_moves.keys())
        black_movable_pieces = set(self.game_board.black_possible_moves.keys())
        actual_movable_pieces = white_movable_pieces.union(black_movable_pieces)

        self.assertEqual(expected_movable_pieces, actual_movable_pieces)


def one_hive_board2():
    # This is copied from test/test_sliding_rules_no_mvt.py
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
    game_board.place_piece('Grasshopper', (-2, -3))  # White
    game_board.place_piece('Ant', (2, 0))  # Black

    return game_board


if __name__ == '__main__':
    unittest.main()
