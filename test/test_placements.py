import unittest

import src.game_board.board as board
import src.game_board.pieces.ant as ant
import src.game_board.pieces.queen_bee as qb
import src.game_board.pieces.grasshopper as gh
import src.game_board.empty_space as emt_spc


class TestInitializationAndPlacements(unittest.TestCase):
    def test_board_is_singleton(self):
        board1 = board.HiveGameBoard()
        board1.test_attribute = 'Test Attribute Values'
        board2 = board.HiveGameBoard()
        self.assertEqual('Test Attribute Value', board2.test_attribute)

    def test_board_initialization(self):
        expected_pieces = dict()
        expected_empty_spaces = {(0, 0): 'Placeholder'}
        expected_white_locs_to_place = {(0, 0)}
        expected_black_locs_to_place = set()
        expected_white_queen_loc = None
        expected_black_queen_loc = None
        expected_is_white_turn = True

        self.assertEqual(expected_pieces.keys(), board.HiveGameBoard().pieces.keys())
        self.assertEqual(expected_empty_spaces.keys(), board.HiveGameBoard().empty_spaces.keys())
        self.assertEqual(expected_white_locs_to_place, board.HiveGameBoard().white_locations_to_place)
        self.assertEqual(expected_black_locs_to_place, board.HiveGameBoard().black_locations_to_place)
        self.assertEqual(expected_white_queen_loc, board.HiveGameBoard().white_queen_location)
        self.assertEqual(expected_black_queen_loc, board.HiveGameBoard().black_queen_location)
        self.assertEqual(expected_is_white_turn, board.HiveGameBoard().is_white_turn())

    def test_create_ant(self):
        # Resets the board
        board.HiveGameBoard(new_board=True)

        ant.Ant(0, 0)

        self._test_new_piece_at_0_0()

        # piece is of type Ant
        new_piece = board.HiveGameBoard().pieces[(0, 0)]
        type_of_piece = str(type(new_piece)).split('.')[-1][:-2]
        self.assertEqual('Ant', type_of_piece)

    def test_create_grasshopper(self):
        # Resets the board
        board.HiveGameBoard(new_board=True)

        gh.Grasshopper(0, 0)

        self._test_new_piece_at_0_0()

        # piece is of type Ant
        new_piece = board.HiveGameBoard().pieces[(0, 0)]
        type_of_piece = str(type(new_piece)).split('.')[-1][:-2]
        self.assertEqual('Grasshopper', type_of_piece)

    def test_create_white_queen_bee(self):
        # Resets the board
        board.HiveGameBoard(new_board=True)

        qb.QueenBee(0, 0)

        expected_stored_qb_loc = (0, 0)
        actual_stored_qb_loc = board.HiveGameBoard().white_queen_location
        self.assertEqual(expected_stored_qb_loc, actual_stored_qb_loc)

        self._test_new_piece_at_0_0()

        # piece is of type Ant
        new_piece = board.HiveGameBoard().pieces[(0, 0)]
        type_of_piece = str(type(new_piece)).split('.')[-1][:-2]
        self.assertEqual('QueenBee', type_of_piece)

    def test_create_black_queen_bee(self):
        # Resets the board
        board.HiveGameBoard(new_board=True)

        qb.QueenBee(0, 0, is_white=False)

        expected_stored_qb_loc = (0, 0)
        actual_stored_qb_loc = board.HiveGameBoard().black_queen_location
        self.assertEqual(expected_stored_qb_loc, actual_stored_qb_loc)

        self._test_new_piece_at_0_0(expected_num_white_connected=0, expected_num_black_connected=1)

        # piece is of type Ant
        new_piece = board.HiveGameBoard().pieces[(0, 0)]
        type_of_piece = str(type(new_piece)).split('.')[-1][:-2]
        self.assertEqual('QueenBee', type_of_piece)

    def _test_new_piece_at_0_0(self, expected_num_white_connected=1, expected_num_black_connected=0):
        # Empty space at (0, 0) was removed
        self.assertFalse((0, 0) in board.HiveGameBoard().empty_spaces)

        # piece was added at (0, 0)
        self.assertTrue((0, 0) in board.HiveGameBoard().pieces)

        # New empty spaces have been added
        expected_empty_spaces = {(-1, -1), (0, -1), (-1, 0), (1, 0), (0, 1), (1, 1)}
        self.assertEqual(expected_empty_spaces, board.HiveGameBoard().empty_spaces.keys())

        # Ensure piece has been connected to empty spaces
        expected_ant_emt_spc_connections = {(-1, -1), (0, -1), (-1, 0), (1, 0), (0, 1), (1, 1)}
        actual_emt_spc_connections = board.HiveGameBoard().pieces[(0, 0)].connected_empty_spaces
        self.assertEqual(expected_ant_emt_spc_connections, actual_emt_spc_connections)

        # Ensure each empty space recorded the correct number of white/black pieces
        for space in actual_emt_spc_connections:
            actual_num_white_connected = board.HiveGameBoard().empty_spaces[space].num_white_connected
            self.assertEqual(expected_num_white_connected, actual_num_white_connected)
            actual_num_black_connected = board.HiveGameBoard().empty_spaces[space].num_black_connected
            self.assertEqual(expected_num_black_connected, actual_num_black_connected)

        expected_piece_connections = {(0, 0)}

        # Ensure proper connections for new empty space at (-1, -1)
        expected_emt_spc_connections = {(0, -1), (-1, 0)}
        actual_emt_spc_connections = board.HiveGameBoard().empty_spaces[(-1, -1)].connected_empty_spaces
        actual_piece_connections = board.HiveGameBoard().empty_spaces[(-1, -1)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (0, -1)
        expected_emt_spc_connections = {(-1, -1), (1, 0)}
        actual_emt_spc_connections = board.HiveGameBoard().empty_spaces[(0, -1)].connected_empty_spaces
        actual_piece_connections = board.HiveGameBoard().empty_spaces[(0, -1)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (-1, 0)
        expected_emt_spc_connections = {(-1, -1), (0, 1)}
        actual_emt_spc_connections = board.HiveGameBoard().empty_spaces[(-1, 0)].connected_empty_spaces
        actual_piece_connections = board.HiveGameBoard().empty_spaces[(-1, 0)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (1, 0)
        expected_emt_spc_connections = {(0, -1), (1, 1)}
        actual_emt_spc_connections = board.HiveGameBoard().empty_spaces[(1, 0)].connected_empty_spaces
        actual_piece_connections = board.HiveGameBoard().empty_spaces[(1, 0)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (0, 1)
        expected_emt_spc_connections = {(-1, 0), (1, 1)}
        actual_emt_spc_connections = board.HiveGameBoard().empty_spaces[(0, 1)].connected_empty_spaces
        actual_piece_connections = board.HiveGameBoard().empty_spaces[(0, 1)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)

        # Ensure proper connections for new empty space at (1, 1)
        expected_emt_spc_connections = {(1, 0), (0, 1)}
        actual_emt_spc_connections = board.HiveGameBoard().empty_spaces[(1, 1)].connected_empty_spaces
        actual_piece_connections = board.HiveGameBoard().empty_spaces[(1, 1)].connected_pieces
        self.assertEqual(expected_piece_connections, actual_piece_connections)
        self.assertEqual(expected_emt_spc_connections, actual_emt_spc_connections)


if __name__ == '__main__':
    unittest.main()
