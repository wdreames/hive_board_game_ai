import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestWhitePlacementErrors(unittest.TestCase):

    def test_no_queen_turn_4(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 2), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -2), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 3), piece_type=spaces.Piece.BEETLE)
        self.assertRaisesRegex(
            RuntimeError,
            'Illegal action. You must place your Queen Bee by your fourth turn.',
            game_board.perform_action,
            game_board.PLACE_PIECE,
            (0, -3),
            piece_type=spaces.Piece.GRASSHOPPER
        )

    def test_invalid_piece_type(self):
        bad_piece_type = 'BadPiece'
        game_board = board.HiveGameBoard(new_board=True)
        self.assertRaisesRegex(
            RuntimeError,
            f'Illegal action. {bad_piece_type} is not a valid type of piece.',
            game_board.perform_action,
            game_board.PLACE_PIECE,
            (0, -3),
            piece_type=bad_piece_type,
        )

    def test_piece_not_available(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 2), piece_type=spaces.Piece.BEETLE)
        self.assertRaisesRegex(
            RuntimeError,
            f'Illegal action. White does not have any more Beetles to place.',
            game_board.perform_action,
            game_board.PLACE_PIECE,
            (0, -2),
            piece_type=spaces.Piece.BEETLE,
        )

    def test_invalid_location(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.BEETLE)

        player = 'White'
        invalid_location = (1, 1)
        self.assertRaisesRegex(
            RuntimeError,
            f'[Illegal action. {player} cannot place a piece at {invalid_location}.]',
            game_board.perform_action,
            game_board.PLACE_PIECE,
            invalid_location,
            piece_type=spaces.Piece.BEETLE,
        )


class TestWhiteMoveErrors(unittest.TestCase):

    def test_cannot_move_without_queen(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.SPIDER)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.ANT)
        self.assertRaisesRegex(
            RuntimeError,
            'Illegal action. You must place your Queen Bee before you can perform a move action.',
            game_board.perform_action,
            game_board.MOVE_PIECE,
            (0, 0),
            new_location=(1, 1)
        )

    def test_attempt_black_move_as_white(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.QUEEN_BEE)
        self.assertRaisesRegex(
            RuntimeError,
            "Illegal action. It is white's turn, but a move for black was attempted.",
            game_board.perform_action,
            game_board.MOVE_PIECE,
            (0, 1),
            new_location=(1, 1)
        )

    def test_one_hive_rule(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 2), piece_type=spaces.Piece.ANT)
        self.assertRaisesRegex(
            RuntimeError,
            'Illegal action. This piece cannot move based on the "One Hive" rule.',
            game_board.perform_action,
            game_board.MOVE_PIECE,
            (0, 0),
            new_location=(1, 1)
        )

    def test_invalid_move(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.QUEEN_BEE)
        self.assertRaisesRegex(
            RuntimeError,
            "Illegal action. This piece cannot move to the specified location.",
            game_board.perform_action,
            game_board.MOVE_PIECE,
            (0, 0),
            new_location=(0, 2)
        )


class TestBlackPlacementErrors(unittest.TestCase):

    def test_no_queen_turn_4(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 2), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -2), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 3), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -3), piece_type=spaces.Piece.ANT)
        self.assertRaisesRegex(
            RuntimeError,
            'Illegal action. You must place your Queen Bee by your fourth turn.',
            game_board.perform_action,
            game_board.PLACE_PIECE,
            (0, 4),
            piece_type=spaces.Piece.GRASSHOPPER
        )

    def test_invalid_piece_type(self):
        bad_piece_type = 'BadPiece'
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.QUEEN_BEE)
        self.assertRaisesRegex(
            RuntimeError,
            f'Illegal action. {bad_piece_type} is not a valid type of piece.',
            game_board.perform_action,
            game_board.PLACE_PIECE,
            (0, -3),
            piece_type=bad_piece_type,
        )

    def test_piece_not_available(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.BEETLE)
        self.assertRaisesRegex(
            RuntimeError,
            f'Illegal action. Black does not have any more Queen Bees to place.',
            game_board.perform_action,
            game_board.PLACE_PIECE,
            (0, 2),
            piece_type=spaces.Piece.QUEEN_BEE,
        )

    def test_invalid_location(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.BEETLE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.BEETLE)

        player = 'Black'
        invalid_location = (1, 1)
        self.assertRaisesRegex(
            RuntimeError,
            f'[Illegal action. {player} cannot place a piece at {invalid_location}.]',
            game_board.perform_action,
            game_board.PLACE_PIECE,
            invalid_location,
            piece_type=spaces.Piece.BEETLE,
        )


class TestBlackMoveErrors(unittest.TestCase):

    def test_cannot_move_without_queen(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.SPIDER)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.SPIDER)
        self.assertRaisesRegex(
            RuntimeError,
            'Illegal action. You must place your Queen Bee before you can perform a move action.',
            game_board.perform_action,
            game_board.MOVE_PIECE,
            (0, 1),
            new_location=(1, 1)
        )

    def test_attempt_white_move_as_black(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.ANT)
        self.assertRaisesRegex(
            RuntimeError,
            "Illegal action. It is black's turn, but a move for white was attempted.",
            game_board.perform_action,
            game_board.MOVE_PIECE,
            (0, -1),
            new_location=(1, 0)
        )

    def test_one_hive_rule(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 2), piece_type=spaces.Piece.ANT)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -2), piece_type=spaces.Piece.ANT)
        self.assertRaisesRegex(
            RuntimeError,
            'Illegal action. This piece cannot move based on the "One Hive" rule.',
            game_board.perform_action,
            game_board.MOVE_PIECE,
            (0, 1),
            new_location=(1, 1)
        )

    def test_invalid_move(self):
        game_board = board.HiveGameBoard(new_board=True)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 0), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, 1), piece_type=spaces.Piece.QUEEN_BEE)
        game_board.perform_action(game_board.PLACE_PIECE, (0, -1), piece_type=spaces.Piece.ANT)
        self.assertRaisesRegex(
            RuntimeError,
            "Illegal action. This piece cannot move to the specified location.",
            game_board.perform_action,
            game_board.MOVE_PIECE,
            (0, 1),
            new_location=(0, -2)
        )


class TestPerformBadAction(unittest.TestCase):

    def test_perform_bad_action(self):
        game_board = board.HiveGameBoard(new_board=True)

        self.assertRaisesRegex(
            ValueError,
            "Action type can only be MOVE_PIECE or PLACE_PIECE.",
            game_board.perform_action,
            'Invalid action type',
            (0, 0),
            piece_type=spaces.Piece.QUEEN_BEE
        )


if __name__ == '__main__':
    unittest.main()
