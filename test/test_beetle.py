import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestBeetle(unittest.TestCase):

    def test_beetle1(self):
        # Test moves for Beetle at (1, -1)
        beetle_board1()

        expected_possible_moves = {(0, -1), (0, -2), (1, -2), (1, 0)}
        actual_possible_moves = board.HiveGameBoard().pieces[(1, -1)].possible_moves
        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_beetle2(self):
        # Test moves for Beetle at (-1, 1)
        beetle_board1()

        expected_possible_moves = {(-1, 0), (0, 1), (0, 2), (-1, 2)}
        actual_possible_moves = board.HiveGameBoard().pieces[(-1, 1)].possible_moves
        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_beetle_on_grasshopper1(self):
        beetle_board1()

        # Move onto Grasshopper
        board.HiveGameBoard().move_piece((1, -1), (0, -1))

        # Move other Pieces
        board.HiveGameBoard().move_piece((0, 2), (1, 2))
        board.HiveGameBoard().move_piece((0, -2), (-1, -2))

        expected_beetle_moves = {(-1, -1), (-1, -2), (0, -2), (1, -1), (1, 0), (0, 0)}
        actual_beetle_moves = board.HiveGameBoard().pieces[(0, -1)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        # Move off of Grasshopper
        board.HiveGameBoard().move_piece((0, -1), (0, 0))

        expected_grasshopper_moves = {(0, 2), (-2, -3)}
        actual_grasshopper_moves = board.HiveGameBoard().pieces[(0, -1)].possible_moves
        self.assertEqual(expected_grasshopper_moves, actual_grasshopper_moves)

    def test_beetle_on_grasshopper2(self):
        # TODO: [Beetle] Also test:
        #       - Move Beetle onto Piece on Grasshopper path
        #       - Move Beetle off Piece
        #       - Move Piece
        #       - Check Grasshopper movement
        beetle_board1()

    def test_beetle_on_spider(self):
        beetle_board1()

        # Make move for Black
        board.HiveGameBoard().place_piece(spaces.Piece.ANT, (2, 0))

        # Move onto Spider
        board.HiveGameBoard().move_piece((-1, 1), (0, 1))

        # Move other pieces
        board.HiveGameBoard().move_piece((0, 2), (1, 2))
        board.HiveGameBoard().move_piece((2, 0), (-1, 0))

        # Move off Spider
        board.HiveGameBoard().move_piece((0, 1), (0, 0))

        board.HiveGameBoard().print_board()

        # Test Spider movement
        expected_spider_moves = {(-2, -1), (2, 3)}
        actual_spider_moves = board.HiveGameBoard().pieces[(0, 1)].possible_moves
        self.assertEqual(expected_spider_moves, actual_spider_moves)

    def test_beetle_on_ant(self):
        beetle_board2()

        # Move onto Ants
        board.HiveGameBoard().move_piece((-2, -3), (-3, -3))
        board.HiveGameBoard().move_piece((2, 0), (3, 0))

        # Move off of Ant
        board.HiveGameBoard().move_piece((-3, -3), (-2, -2))
        board.HiveGameBoard().move_piece((3, 0), (4, 0))

        expected_ant_moves1 = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-2, -1), (-1, -1), (-4, -4), (-3, -4)})
        expected_ant_moves2 = set(board.HiveGameBoard().empty_spaces.keys()).difference(
            {(-2, -1), (-1, -1), (2, 0), (3, 1)})
        actual_ant_moves1 = board.HiveGameBoard().pieces[(-3, -3)].possible_moves
        actual_ant_moves2 = board.HiveGameBoard().pieces[(3, 0)].possible_moves

        self.assertEqual(expected_ant_moves1, actual_ant_moves1)
        self.assertEqual(expected_ant_moves2, actual_ant_moves2)

    def test_beetle_on_queen_bee(self):
        beetle_board1()

        # Move onto Queen Bee
        board.HiveGameBoard().move_piece((1, -1), (0, -2))

        # White move
        board.HiveGameBoard().move_piece((0, 2), (1, 2))

        # Move off of Queen Bee
        board.HiveGameBoard().move_piece((0, -2), (-1, -3))

        expected_qb_moves = {(0, -3), (1, -1)}
        actual_qb_moves = board.HiveGameBoard().pieces[(0, -2)].possible_moves
        self.assertEqual(expected_qb_moves, actual_qb_moves)

    def test_beetle_on_queen_bee_win(self):
        pass

    def test_beetle_stack(self):
        pass


def beetle_board1():
    game_board = board.HiveGameBoard(new_board=True)
    ant = spaces.Piece.ANT
    beetle = spaces.Piece.BEETLE
    grasshopper = spaces.Piece.GRASSHOPPER
    queen_bee = spaces.Piece.QUEEN_BEE
    spider = spaces.Piece.SPIDER

    game_board.place_piece(ant, (0, 0))  # White
    game_board.place_piece(grasshopper, (0, -1))  # Black
    game_board.place_piece(spider, (0, 1))  # White
    game_board.place_piece(queen_bee, (0, -2))  # Black
    game_board.place_piece(queen_bee, (0, 2))  # White
    game_board.place_piece(beetle, (1, -1))  # Black
    game_board.place_piece(beetle, (-1, 1))  # White

    game_board.print_board()


def beetle_board2():
    game_board = board.HiveGameBoard(new_board=True)
    ant = spaces.Piece.ANT
    beetle = spaces.Piece.BEETLE
    grasshopper = spaces.Piece.GRASSHOPPER
    queen_bee = spaces.Piece.QUEEN_BEE
    spider = spaces.Piece.SPIDER

    # Make moves for a sample game
    game_board.place_piece(grasshopper, (0, 0))  # White
    game_board.place_piece(grasshopper, (0, -1))  # Black
    game_board.place_piece(grasshopper, (-1, 0))  # White
    game_board.place_piece(queen_bee, (0, -2))  # Black
    game_board.place_piece(ant, (-2, 0))  # White
    game_board.place_piece(ant, (1, -2))  # Black
    game_board.place_piece(queen_bee, (-3, -1))  # White
    game_board.place_piece(grasshopper, (2, -2))  # Black
    game_board.place_piece(spider, (-3, -2))  # White
    game_board.place_piece(spider, (3, -1))  # Black
    game_board.place_piece(ant, (-3, -3))  # White
    game_board.place_piece(ant, (3, 0))  # Black
    game_board.place_piece(beetle, (-2, -3))  # White
    game_board.place_piece(beetle, (2, 0))  # Black

    game_board.print_board()


if __name__ == '__main__':
    unittest.main()
