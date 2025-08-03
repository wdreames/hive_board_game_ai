from io import StringIO
import os
import pickle
import sys
import unittest
from unittest.mock import patch
from src import agents
import src.game.board as board
import src.game.spaces as spaces


class TestFailedGames(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manager = board.BoardManager()

    def _load_game(self, file_name):
        file_path = os.path.join('test', 'data', file_name)
        with open(file_path, 'rb') as file:
            game_state = pickle.load(file)
            self.manager.current_board = game_state

        self.manager.get_board().print_board(hex_board=False)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_output(self, mock_stdout):
        self._load_game('failed_game_2.hv')
        minimax_agent = agents.MinimaxAI(self.manager, max_depth=2, is_white=False, save_state_on_errors=False)
        minimax_agent.get_action()
        print_output = mock_stdout.getvalue()
        self.assertNotIn('An error occurred while processing evaluations for the action', print_output, f'An error occurred while processing evaluations:\n{print_output}')

if __name__ == '__main__':
    unittest.main()
