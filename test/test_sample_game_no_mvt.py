import unittest
import src.game_board.board as board


class TestSampleGameWithNoMovement(unittest.TestCase):

    # Goals with this test:
    # Only use the board to interact with / alter pieces and empty spaces
    # X Check turn order
    # X Ensure piece colors are correct
    # X Ensure queen bee on 4th move
    # X Ensure all empty spaces are available for placement on moves 1 and 2
    # Assert that all empty spaces and their connections are correct
    # Assert that all pieces and their connections are correct
    # X Assert correct locations for placement
    # NOTE: Assertions will not need to happen on every turn, use once in middle and once at end
    # X Ensure piece limits
    # Check for locking pieces
    # X Check for game won (player will need to surround their own queen)

    # TODO: [Testing] I could probably split a lot of these into multiple test cases

    @classmethod
    def setUpClass(cls):
        board.HiveGameBoard(new_board=True)
        cls.expected_white_pieces_to_place = board.HiveGameBoard().white_pieces_to_place
        cls.expected_black_pieces_to_place = board.HiveGameBoard().black_pieces_to_place

    def test_0_players_have_same_pieces(self):
        board.HiveGameBoard(new_board=True)
        self.assertEqual(board.HiveGameBoard().white_pieces_to_place, board.HiveGameBoard().black_pieces_to_place)

    def test_1_start_game(self):
        board.HiveGameBoard(new_board=True)

        # Check that white has all moves available
        expected_available_moves = {(0, 0)}
        _, actual_available_moves = board.HiveGameBoard().get_all_possible_placements()
        self.assertEqual(expected_available_moves, actual_available_moves)

        board.HiveGameBoard().place_piece('Ant', (0, 0))  # White

        # Check that black has all moves available
        expected_avaiable_moves = {(-1, -1), (0, -1), (-1, 0), (1, 0), (0, 1), (1, 1)}
        _, actual_available_moves = board.HiveGameBoard().get_all_possible_placements()
        self.assertEqual(expected_avaiable_moves, actual_available_moves)

        board.HiveGameBoard().place_piece('Grasshopper', (-1, -1))  # Black

        # Ensure move lists are limited past turn 2
        expected_white_available_moves = {(0, 1), (1, 1), (1, 0)}
        _, actual_white_available_moves = board.HiveGameBoard().get_all_possible_placements()
        self.assertEqual(expected_white_available_moves, actual_white_available_moves)

        board.HiveGameBoard().place_piece('Queen Bee', (0, 1))  # White
        expected_black_available_moves = {(-2, -1), (-2, -2), (-1, -2)}
        _, actual_black_available_moves = board.HiveGameBoard().get_all_possible_placements()
        self.assertEqual(expected_black_available_moves, actual_black_available_moves)

    def test_2_mid_game(self):
        # Continue placing pieces
        board.HiveGameBoard().place_piece('Ant', (-1, -2))  # Black
        board.HiveGameBoard().place_piece('Ant', (1, 2))  # White
        board.HiveGameBoard().place_piece('Ant', (-2, -3))  # Black

        # Each player has made 3 moves; Should be turn 7 now
        expected_turn_number = 7
        actual_turn_number = board.HiveGameBoard().turn_number
        self.assertEqual(expected_turn_number, actual_turn_number)

        # Ensure correct number of remaining pieces to place
        self.expected_white_pieces_to_place['Ant'] -= 2
        self.expected_white_pieces_to_place['Queen Bee'] -= 1
        self.expected_black_pieces_to_place['Ant'] -= 2
        self.expected_black_pieces_to_place['Grasshopper'] -= 1
        actual_white_pieces_to_place = board.HiveGameBoard().white_pieces_to_place
        actual_black_pieces_to_place = board.HiveGameBoard().black_pieces_to_place
        self.assertEqual(self.expected_white_pieces_to_place, actual_white_pieces_to_place)
        self.assertEqual(self.expected_black_pieces_to_place, actual_black_pieces_to_place)

        # Check piece locations on the board
        expected_piece_locations = {(0, 0), (-1, -1), (-1, -2), (0, 1), (1, 2), (-2, -3)}
        actual_piece_locations = board.HiveGameBoard().pieces.keys()
        self.assertEqual(expected_piece_locations, actual_piece_locations)

        # Ensure sample white and black pieces are correct colors
        expected_is_white = True
        actual_is_white = board.HiveGameBoard().pieces[(1, 2)].is_white
        self.assertEqual(expected_is_white, actual_is_white)

        expected_is_white = False
        actual_is_white = board.HiveGameBoard().pieces[(-1, -1)].is_white
        self.assertEqual(expected_is_white, actual_is_white)

        # Check stored locations for queen bees
        expected_white_qb_loc = (0, 1)
        actual_white_qb_loc = board.HiveGameBoard().white_queen_location
        self.assertEqual(expected_white_qb_loc, actual_white_qb_loc)

        expected_black_qb_loc = None
        actual_black_qb_loc = board.HiveGameBoard().black_queen_location
        self.assertEqual(expected_black_qb_loc, actual_black_qb_loc)

        # Check empty space locations on the board
        expected_white_available_moves = {(-1, 1), (0, 2), (1, 3), (2, 3), (2, 2), (1, 1), (1, 0)}
        expected_black_available_moves = {(0, -2), (-1, -3), (-2, -4), (-3, -4), (-3, -3), (-2, -2), (-2, -1)}
        expected_emt_spc_locations = {(-1, 0), (0, -1)}.union(expected_white_available_moves).union(
            expected_black_available_moves)
        actual_emt_spc_locations = board.HiveGameBoard().empty_spaces.keys()
        self.assertEqual(expected_emt_spc_locations, actual_emt_spc_locations)

        # Check available moves for white
        actual_white_pieces_to_place, actual_white_available_moves = board.HiveGameBoard().get_all_possible_placements()
        self.assertEqual(self.expected_white_pieces_to_place, actual_white_pieces_to_place)
        self.assertEqual(expected_white_available_moves, actual_white_available_moves)

        # Make a move for white
        board.HiveGameBoard().place_piece('Grasshopper', (2, 2))  # White

        # Check available moves for black
        expected_black_pieces_to_place = {'Queen Bee': 1}  # Queen bee is required to be played <= the player's 4th turn
        actual_black_pieces_to_place, actual_black_available_moves = board.HiveGameBoard().get_all_possible_placements()
        self.assertEqual(expected_black_pieces_to_place, actual_black_pieces_to_place)
        self.assertEqual(expected_black_available_moves, actual_black_available_moves)

        # Ensure no winner yet
        expected_winner = None
        actual_winner = board.HiveGameBoard().determine_winner()
        self.assertEqual(expected_winner, actual_winner)

    def test_3_end_game(self):
        # Continue making moves
        # TODO: [Errors] Maybe make these raise errors and test for those here
        board.HiveGameBoard().place_piece('Ant', (-2, -2))          # Black; Meant to fail & be skipped
        board.HiveGameBoard().place_piece('Queen Bee', (-1, 0))     # Black; Meant to fail & be skipped
        board.HiveGameBoard().place_piece('Queen Bee', (-2, -2))    # Black
        board.HiveGameBoard().place_piece('Queen Bee', (1, 1))      # White; Meant to fail & be skipped
        board.HiveGameBoard().place_piece('Ant', (1, 1))            # White
        board.HiveGameBoard().place_piece('Grasshopper', (-3, -3))  # Black
        board.HiveGameBoard().place_piece('Grasshopper', (2, 1))    # White
        board.HiveGameBoard().place_piece('Grasshopper', (-3, -2))  # Black
        board.HiveGameBoard().place_piece('Grasshopper', (3, 2))    # White
        board.HiveGameBoard().place_piece('Ant', (-2, -1))          # Black

        # Each player has made 7 moves; Should be turn 15 now
        expected_turn_number = 15
        actual_turn_number = board.HiveGameBoard().turn_number
        self.assertEqual(expected_turn_number, actual_turn_number)

        # Check for a winner
        expected_winner = 'white'
        actual_winner = board.HiveGameBoard().determine_winner()
        self.assertEqual(expected_winner, actual_winner)

        board.HiveGameBoard().print_board()


if __name__ == '__main__':
    unittest.main()
