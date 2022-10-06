import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestOneHiveBoard1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game_board = board.HiveGameBoard(new_board=True)
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(ant, (0, 0))
        game_board.place_piece(spider, (1, 1))
        game_board.place_piece(grasshopper, (0, -1))
        game_board.place_piece(beetle, (2, 2))
        game_board.place_piece(queen_bee, (0, -2))
        game_board.place_piece(queen_bee, (2, 1))
        game_board.place_piece(ant, (1, -1))
        game_board.place_piece(grasshopper, (1, 2))
        game_board.place_piece(ant, (-1, 0))

        game_board.move_piece((1, 2), (1, 0))
        game_board.move_piece((-1, 0), (2, 0))

        game_board.print_board()

    def test_all_pieces_can_move(self):
        for piece in board.HiveGameBoard().pieces.values():
            self.assertTrue(piece.can_move)

    def test_all_pieces_in_possible_moves(self):
        expected_movable_pieces = set(board.HiveGameBoard().pieces.keys())

        white_movable_pieces = set(board.HiveGameBoard().white_possible_moves.keys())
        black_movable_pieces = set(board.HiveGameBoard().black_possible_moves.keys())
        actual_movable_pieces = white_movable_pieces.union(black_movable_pieces)

        self.assertEqual(expected_movable_pieces, actual_movable_pieces)


if __name__ == '__main__':
    unittest.main()
