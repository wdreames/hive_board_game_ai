import unittest

import src.game.board as board
import src.game.pieces as pcs


class TestInitializationAndPlacements(unittest.TestCase):

    def test_board_initialization(self):
        game_board = board.HiveGameBoard()
        expected_pieces = dict()
        expected_empty_spaces = {(0, 0): 'Placeholder'}
        expected_white_locs_to_place = {(0, 0)}
        expected_black_locs_to_place = set()
        expected_white_queen_loc = None
        expected_black_queen_loc = None
        expected_is_white_turn = True
        expected_winner = None

        self.assertEqual(expected_pieces.keys(), game_board.pieces.keys())
        self.assertEqual(expected_empty_spaces.keys(), game_board.empty_spaces.keys())
        self.assertEqual(expected_white_locs_to_place, game_board.white_locations_to_place)
        self.assertEqual(expected_black_locs_to_place, game_board.black_locations_to_place)
        self.assertEqual(expected_white_queen_loc, game_board.white_queen_location)
        self.assertEqual(expected_black_queen_loc, game_board.black_queen_location)
        self.assertEqual(expected_is_white_turn, game_board.is_white_turn())
        self.assertEqual(expected_winner, game_board.determine_winner())

    def test_create_ant(self):
        # Resets the board
        game_board = board.HiveGameBoard()

        pcs.Ant(game_board, 0, 0)

        self._test_new_piece_at_0_0(game_board)

        # piece is of type Ant
        new_piece = game_board.pieces[(0, 0)]
        type_of_piece = str(type(new_piece)).split('.')[-1][:-2]
        self.assertEqual('Ant', type_of_piece)

    def test_create_grasshopper(self):
        # Resets the board
        game_board = board.HiveGameBoard()

        pcs.Grasshopper(game_board, 0, 0)

        self._test_new_piece_at_0_0(game_board)

        # piece is of type Ant
        new_piece = game_board.pieces[(0, 0)]
        type_of_piece = str(type(new_piece)).split('.')[-1][:-2]
        self.assertEqual('Grasshopper', type_of_piece)

    def _test_new_piece_at_0_0(self, game_board, expected_num_white_connected=1, expected_num_black_connected=0):
        # Empty space at (0, 0) was removed
        self.assertFalse((0, 0) in game_board.empty_spaces)

        # piece was added at (0, 0)
        self.assertTrue((0, 0) in game_board.pieces)

        # New empty spaces have been added
        expected_empty_spaces = {(-1, -1), (0, -1), (-1, 0), (1, 0), (0, 1), (1, 1)}
        self.assertEqual(expected_empty_spaces, game_board.empty_spaces.keys())

        # Ensure piece has been connected to empty spaces
        expected_ant_emt_spc_connections = {(-1, -1), (0, -1), (-1, 0), (1, 0), (0, 1), (1, 1)}
        actual_emt_spc_connections = game_board.pieces[(0, 0)].connected_empty_spaces
        self.assertEqual(expected_ant_emt_spc_connections, actual_emt_spc_connections)

        # Ensure each empty space recorded the correct number of white/black pieces
        for space in actual_emt_spc_connections:
            actual_num_white_connected = game_board.empty_spaces[space].num_white_connected
            self.assertEqual(expected_num_white_connected, actual_num_white_connected)
            actual_num_black_connected = game_board.empty_spaces[space].num_black_connected
            self.assertEqual(expected_num_black_connected, actual_num_black_connected)

        expected_piece_connections = {(0, 0)}

        # Ensure proper connections for new empty space at (-1, -1)
        expected_emt_spc_connections = {(0, -1), (-1, 0)}
        actual_emt_spc_connections = game_board.empty_spaces[(-1, -1)].connected_empty_spaces
        actual_piece_connections = game_board.empty_spaces[(-1, -1)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (0, -1)
        expected_emt_spc_connections = {(-1, -1), (1, 0)}
        actual_emt_spc_connections = game_board.empty_spaces[(0, -1)].connected_empty_spaces
        actual_piece_connections = game_board.empty_spaces[(0, -1)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (-1, 0)
        expected_emt_spc_connections = {(-1, -1), (0, 1)}
        actual_emt_spc_connections = game_board.empty_spaces[(-1, 0)].connected_empty_spaces
        actual_piece_connections = game_board.empty_spaces[(-1, 0)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (1, 0)
        expected_emt_spc_connections = {(0, -1), (1, 1)}
        actual_emt_spc_connections = game_board.empty_spaces[(1, 0)].connected_empty_spaces
        actual_piece_connections = game_board.empty_spaces[(1, 0)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (0, 1)
        expected_emt_spc_connections = {(-1, 0), (1, 1)}
        actual_emt_spc_connections = game_board.empty_spaces[(0, 1)].connected_empty_spaces
        actual_piece_connections = game_board.empty_spaces[(0, 1)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (1, 1)
        expected_emt_spc_connections = {(1, 0), (0, 1)}
        actual_emt_spc_connections = game_board.empty_spaces[(1, 1)].connected_empty_spaces
        actual_piece_connections = game_board.empty_spaces[(1, 1)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)


if __name__ == '__main__':
    unittest.main()
