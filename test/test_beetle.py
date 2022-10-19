import unittest
import src.game.board as board
import src.game.spaces as spaces


class TestBeetle(unittest.TestCase):

    def test_beetle1(self):
        # Test moves for Beetle at (1, -1)
        game_board = beetle_board1()

        expected_possible_moves = {(0, -1), (0, -2), (1, -2), (1, 0)}
        actual_possible_moves = game_board.pieces[(1, -1)].possible_moves
        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_beetle2(self):
        # Test moves for Beetle at (-1, 1)
        game_board = beetle_board1()

        expected_possible_moves = {(-1, 0), (0, 1), (0, 2), (-1, 2)}
        actual_possible_moves = game_board.pieces[(-1, 1)].possible_moves
        self.assertEqual(expected_possible_moves, actual_possible_moves)

    def test_beetle_on_grasshopper1(self):
        game_board = beetle_board1()

        # Move onto Grasshopper
        game_board.move_piece((1, -1), (0, -1))

        # Move other Pieces
        game_board.move_piece((0, 2), (1, 2))
        game_board.move_piece((0, -2), (-1, -2))
        game_board.move_piece((-1, 1), (0, 1))

        expected_beetle_moves = {(-1, -1), (-1, -2), (0, -2), (1, -1), (1, 0), (0, 0)}
        actual_beetle_moves = game_board.pieces[(0, -1)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        # Move off of Grasshopper
        game_board.print_board()
        game_board.move_piece((0, -1), (0, 0))

        expected_grasshopper_moves = {(0, 2), (-2, -3)}
        actual_grasshopper_moves = game_board.pieces[(0, -1)].possible_moves
        self.assertEqual(expected_grasshopper_moves, actual_grasshopper_moves)

    def test_beetle_on_grasshopper2(self):
        # Move Beetle onto Piece on Grasshopper path
        # Move Grasshopper
        # Move Beetle off Piece
        # Move Piece that used to be on Grasshopper path
        # Check Grasshopper movement
        game_board = beetle_board4()

        expected_grasshopper_moves = {(-1, -1), (-1, -3)}
        actual_grasshopper_moves = game_board.pieces[(1, -1)].possible_moves
        self.assertEqual(expected_grasshopper_moves, actual_grasshopper_moves)

    def test_beetle_on_spider1(self):
        game_board = beetle_board1()

        # Make move for Black
        game_board.place_piece(spaces.Piece.ANT, (2, 0))

        # Move onto Spider
        game_board.move_piece((-1, 1), (0, 1))

        # Move other pieces
        game_board.move_piece((2, 0), (-1, 0))
        game_board.move_piece((0, 2), (1, 2))
        game_board.move_piece((1, -1), (1, 0))

        game_board.print_board()

        # Move off Spider
        game_board.move_piece((0, 1), (0, 0))

        game_board.print_board()

        # Test Spider movement
        expected_spider_moves = {(-2, -1), (2, 3)}
        actual_spider_moves = game_board.pieces[(0, 1)].possible_moves
        self.assertEqual(expected_spider_moves, actual_spider_moves)

    def test_beetle_on_spider2(self):
        game_board = beetle_board3()

        expected_spider_moves = {(-3, -1), (0, -2)}
        actual_spider_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_spider_moves, actual_spider_moves)

    def test_beetle_on_ant(self):
        game_board = beetle_board2()

        # Move onto Ants
        game_board.move_piece((-2, -3), (-3, -3))
        game_board.move_piece((2, 0), (3, 0))

        # Move off of Ant
        game_board.move_piece((-3, -3), (-2, -2))
        game_board.move_piece((3, 0), (4, 0))

        expected_ant_moves1 = set(game_board.empty_spaces.keys()).difference(
            {(-2, -1), (-1, -1), (-4, -4), (-3, -4)})
        expected_ant_moves2 = set(game_board.empty_spaces.keys()).difference(
            {(-2, -1), (-1, -1), (2, 0), (3, 1)})
        actual_ant_moves1 = game_board.pieces[(-3, -3)].possible_moves
        actual_ant_moves2 = game_board.pieces[(3, 0)].possible_moves

        self.assertEqual(expected_ant_moves1, actual_ant_moves1)
        self.assertEqual(expected_ant_moves2, actual_ant_moves2)

    def test_beetle_on_queen_bee(self):
        game_board = beetle_board1()

        # Move onto Queen Bee
        game_board.move_piece((1, -1), (0, -2))

        # White move
        game_board.move_piece((0, 2), (1, 2))

        # Move off of Queen Bee
        game_board.move_piece((0, -2), (-1, -3))

        expected_qb_moves = {(0, -3), (1, -1)}
        actual_qb_moves = game_board.pieces[(0, -2)].possible_moves
        self.assertEqual(expected_qb_moves, actual_qb_moves)

    def test_beetle_on_queen_bee_win(self):
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        # Make moves for a sample game
        game_board.place_piece(queen_bee, (0, 0))
        game_board.place_piece(beetle, (0, 1))
        game_board.place_piece(ant, (0, -1))
        game_board.place_piece(queen_bee, (1, 2))
        game_board.place_piece(spider, (0, -2))
        game_board.move_piece((1, 2), (1, 1))
        game_board.place_piece(grasshopper, (0, -3))

        # Move black beetle onto white queen bee, then begin placing pieces around the queen bee
        game_board.move_piece((0, 1), (0, 0))
        game_board.place_piece(beetle, (0, -4))
        game_board.place_piece(ant, (0, 1))
        game_board.place_piece(ant, (0, -5))
        game_board.place_piece(ant, (-1, 1))
        game_board.place_piece(beetle, (0, -6))
        game_board.move_piece((-1, 1), (1, 0))
        game_board.place_piece(grasshopper, (0, -7))
        game_board.place_piece(beetle, (-1, 1))
        game_board.place_piece(ant, (0, -8))
        game_board.move_piece((-1, 1), (-1, 0))
        game_board.place_piece(spider, (0, -9))
        game_board.place_piece(ant, (-1, 1))
        game_board.place_piece(grasshopper, (0, -10))
        game_board.move_piece((-1, 1), (-1, -1))

        game_board.print_board()

        expected_winner_result = board.HiveGameBoard.BLACK_WINNER
        actual_winner_result = game_board.determine_winner()
        self.assertEqual(expected_winner_result, actual_winner_result)

    def test_beetle_stack_on_grasshopper(self):
        # Ensure no errors occur when stacking/unstacking multiple beetles
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        # Set up the board
        game_board.place_piece(grasshopper, (0, 0))
        game_board.place_piece(beetle, (1, 0))
        game_board.place_piece(beetle, (-1, 0))
        game_board.place_piece(beetle, (2, 1))
        game_board.place_piece(beetle, (-2, 0))
        game_board.place_piece(queen_bee, (1, -1))
        game_board.place_piece(queen_bee, (-1, 1))

        # Move the pieces
        game_board.move_piece((1, -1), (0, -1))
        game_board.move_piece((-1, 1), (0, 1))

        game_board.move_piece((2, 1), (1, 1))
        game_board.move_piece((-2, 0), (-1, 0))
        game_board.move_piece((1, 1), (0, 0))
        game_board.move_piece((-1, 0), (0, 0))
        game_board.move_piece((1, 0), (0, 0))
        game_board.move_piece((-1, 0), (0, 0))

        expected_beetle_moves = {(-1, -1), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 0)}
        actual_beetle_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        # Move the queen bees
        game_board.move_piece((0, -1), (1, 0))
        game_board.move_piece((0, 1), (1, 1))
        game_board.move_piece((1, 0), (2, 1))

        # Begin moving beetles off the stack
        game_board.move_piece((0, 0), (0, 1))
        expected_beetle_moves = {(-1, -1), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 0)}
        actual_beetle_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        game_board.move_piece((0, 0), (0, -1))
        expected_beetle_moves = {(-1, -1), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 0)}
        actual_beetle_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        game_board.move_piece((0, 0), (0, -1))
        expected_beetle_moves = {(-1, -1), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 0)}
        actual_beetle_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        game_board.move_piece((0, 0), (1, 1))

        game_board.print_board()

        # Check the moves of the grasshopper
        expected_grasshopper_moves = {(0, 2), (0, -2), (2, 2)}
        actual_grasshopper_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_grasshopper_moves, actual_grasshopper_moves)

    def test_beetle_stack_on_spider(self):
        # Ensure no errors occur when stacking/unstacking multiple beetles
        game_board = board.HiveGameBoard()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER

        # Set up the board
        game_board.place_piece(spider, (0, 0))
        game_board.place_piece(beetle, (1, 0))
        game_board.place_piece(beetle, (-1, 0))
        game_board.place_piece(beetle, (2, 1))
        game_board.place_piece(beetle, (-2, 0))
        game_board.place_piece(queen_bee, (1, -1))
        game_board.place_piece(queen_bee, (-1, 1))

        # Move the pieces
        game_board.move_piece((1, -1), (0, -1))
        game_board.move_piece((-1, 1), (0, 1))

        game_board.move_piece((2, 1), (1, 1))
        game_board.move_piece((-2, 0), (-1, 0))
        game_board.move_piece((1, 1), (0, 0))
        game_board.move_piece((-1, 0), (0, 0))
        game_board.move_piece((1, 0), (0, 0))
        game_board.move_piece((-1, 0), (0, 0))

        expected_beetle_moves = {(-1, -1), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 0)}
        actual_beetle_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        # Move the queen bees
        game_board.move_piece((0, -1), (1, 0))
        game_board.move_piece((0, 1), (1, 1))
        game_board.move_piece((1, 0), (2, 1))

        # Begin moving beetles off the stack
        game_board.move_piece((0, 0), (1, 0))
        expected_beetle_moves = {(-1, -1), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 0)}
        actual_beetle_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        game_board.move_piece((0, 0), (0, -1))
        expected_beetle_moves = {(-1, -1), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 0)}
        actual_beetle_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        game_board.move_piece((0, 0), (0, -1))
        expected_beetle_moves = {(-1, -1), (0, -1), (1, 0), (1, 1), (0, 1), (-1, 0)}
        actual_beetle_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)

        game_board.move_piece((0, 0), (1, 1))

        game_board.print_board()

        # Check the moves of the grasshopper
        expected_beetle_moves = {(2, 2), (0, -2)}
        actual_beetle_moves = game_board.pieces[(0, 0)].possible_moves
        self.assertEqual(expected_beetle_moves, actual_beetle_moves)


def beetle_board1():
    game_board = board.HiveGameBoard()
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

    return game_board


def beetle_board2():
    game_board = board.HiveGameBoard()
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

    return game_board


def beetle_board3():
    game_board = board.HiveGameBoard()
    ant = spaces.Piece.ANT
    beetle = spaces.Piece.BEETLE
    grasshopper = spaces.Piece.GRASSHOPPER
    queen_bee = spaces.Piece.QUEEN_BEE
    spider = spaces.Piece.SPIDER

    # Make moves for a sample game
    game_board.place_piece(spider, (0, 0))
    game_board.place_piece(beetle, (0, 1))
    game_board.place_piece(queen_bee, (-1, -1))

    game_board.place_piece(queen_bee, (1, 2))
    game_board.move_piece((-1, -1), (-1, 0))
    game_board.move_piece((1, 2), (1, 1))
    game_board.move_piece((-1, 0), (-1, -1))

    game_board.move_piece((0, 1), (0, 0))
    game_board.place_piece(ant, (-2, -2))

    game_board.move_piece((1, 1), (1, 0))
    game_board.move_piece((-2, -2), (-1, 0))
    game_board.move_piece((1, 0), (0, -1))
    game_board.move_piece((-1, 0), (-2, -1))
    game_board.move_piece((0, 0), (0, -1))

    game_board.print_board()

    return game_board


def beetle_board4():
    game_board = board.HiveGameBoard()
    ant = spaces.Piece.ANT
    beetle = spaces.Piece.BEETLE
    grasshopper = spaces.Piece.GRASSHOPPER
    queen_bee = spaces.Piece.QUEEN_BEE
    spider = spaces.Piece.SPIDER

    # Make moves for a sample game
    game_board.place_piece(ant, (0, 0))
    game_board.place_piece(grasshopper, (-1, -1))
    game_board.place_piece(queen_bee, (1, 1))
    game_board.place_piece(queen_bee, (-1, -2))
    game_board.place_piece(beetle, (0, 1))
    game_board.move_piece((-1, -2), (0, -1))

    # Move Beetle onto Piece on Grasshopper path
    game_board.move_piece((0, 1), (1, 1))

    # Move the Grasshopper
    game_board.move_piece((-1, -1), (1, -1))

    # Move the Beetle off of the Piece
    game_board.move_piece((1, 1), (0, 1))

    game_board.place_piece(beetle, (0, -2))

    # Move the Piece that used to be on the Grasshopper path
    game_board.move_piece((1, 1), (1, 2))

    return game_board


if __name__ == '__main__':
    unittest.main()
