import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestSampleGameDraw(unittest.TestCase):

    def test_sample_game_draw(self):
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        game_board.place_piece(queen_bee, (0, 0))
        game_board.place_piece(queen_bee, (1, 0))
        game_board.place_piece(beetle, (-1, 0))
        game_board.place_piece(beetle, (2, 0))
        game_board.place_piece(ant, (0, 1))
        game_board.place_piece(ant, (1, -1))
        game_board.place_piece(ant, (-1, -1))
        game_board.place_piece(ant, (2, 1))

        game_board.move_piece((-1, 0), (0, 0))
        game_board.move_piece((2, 0), (1, 0))

        game_board.place_piece(ant, (-1, 0))
        game_board.place_piece(ant, (2, 0))

        game_board.print_board()

        expected_winner = None
        actual_winner = game_board.determine_winner()
        self.assertEqual(expected_winner, actual_winner)

        game_board.move_piece((0, 0), (0, -1))
        game_board.print_board()

        expected_winner = None
        actual_winner = game_board.determine_winner()
        self.assertEqual(expected_winner, actual_winner)

        game_board.move_piece((1, 0), (1, 1))
        game_board.print_board()

        expected_winner = board.HiveGameBoard.DRAW
        actual_winner = game_board.determine_winner()
        self.assertEqual(expected_winner, actual_winner)
