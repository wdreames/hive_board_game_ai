import unittest
from src import agents
import src.game.board as board
import src.game.spaces as spaces


class TestMinimaxEval(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.manager = board.BoardManager()
        
        game_board = cls.manager.get_board()
        ant = spaces.Piece.ANT
        beetle = spaces.Piece.BEETLE
        grasshopper = spaces.Piece.GRASSHOPPER
        queen_bee = spaces.Piece.QUEEN_BEE
        spider = spaces.Piece.SPIDER
        
        game_board.place_piece(beetle, (0,0))
        game_board.place_piece(grasshopper, (-1,-1))
        game_board.place_piece(ant, (1,1))
        game_board.place_piece(ant, (-2,-1))
        game_board.place_piece(queen_bee, (0, 1))
        game_board.place_piece(queen_bee, (-2,-2))
        game_board.move_piece((1,1), (-2,-3))
        game_board.place_piece(ant, (-3,-2))
        game_board.move_piece((-2,-3), (-4,-2))
        game_board.move_piece((-2,-1), (0,2))
        game_board.place_piece(ant, (-5, -2))
        game_board.move_piece((0,2), (-6,-2))
        game_board.place_piece(ant, (0,2))
        game_board.place_piece(beetle, (-2,-1))
        game_board.move_piece((0,2), (-2,-3))
        game_board.move_piece((-2,-1), (-1,-1))
        game_board.place_piece(grasshopper, (-3,-4))
        game_board.move_piece((-1,-1), (0,0))
        game_board.place_piece(grasshopper, (-3,-5))
        game_board.move_piece((0,0), (0, 1))
        game_board.move_piece((-3,-5), (-3,-3))
        game_board.place_piece(grasshopper, (0,2))
        game_board.place_piece(grasshopper, (-2,-4))
        game_board.place_piece(ant, (-1, 1))
        game_board.move_piece((-2,-4), (-2, -1))
        game_board.move_piece((-1, 1), (-4,-5))

        game_board.print_board(hex_board=False)

    def test_minimax_cannot_find_win(self):
        game_board = self.manager.get_board()
        game_board.place_piece(spaces.Piece.BEETLE, (-2, -4))
        game_board.place_piece(spaces.Piece.SPIDER, (-4,-6))
        game_board.place_piece(spaces.Piece.SPIDER, (-2, -5))

        # At this point the opponent cannot stop victory. Confirm that a win can be found no matter what move the opponent makes.
        all_opponent_actions_result_in_win = True
        for action in game_board.get_action_list():
            game_board.perform_action(action)
            if not agents.MinimaxAI.find_win(game_board, white_to_move=True):
                all_opponent_actions_result_in_win = False
            game_board.undo_action(action)
        
        self.assertFalse(all_opponent_actions_result_in_win)

    def test_minimax_cannot_find_win_2(self):
        game_board = self.manager.get_board()
        game_board.place_piece(spaces.Piece.BEETLE, (-2, -4))
        game_board.place_piece(spaces.Piece.SPIDER, (-4,-6))
        game_board.move_piece((-2, -4), (-1, -3))

        # At this point the opponent cannot stop victory. Confirm that a win can be found no matter what move the opponent makes.
        all_opponent_actions_result_in_win = True
        for action in game_board.get_action_list():
            game_board.perform_action(action)
            if not agents.MinimaxAI.find_win(game_board, white_to_move=True):
                all_opponent_actions_result_in_win = False
            game_board.undo_action(action)
        
        self.assertFalse(all_opponent_actions_result_in_win)

    def test_minimax_find_win(self):
        game_board = self.manager.get_board()
        game_board.place_piece(spaces.Piece.BEETLE, (-2, -4))
        game_board.place_piece(spaces.Piece.SPIDER, (-4,-6))
        game_board.move_piece((-2,-4), (-2,-3))

        # At this point the opponent cannot stop victory. Confirm that a win can be found no matter what move the opponent makes.
        for action in game_board.get_action_list():
            game_board.perform_action(action)
            self.assertTrue(agents.MinimaxAI.find_win(game_board, white_to_move=True), f'Unable to find win after opponent took the following action: {action}')
            game_board.undo_action(action)

    def test_minimax_depth_1_find_win(self):
        game_board = self.manager.get_board()
        game_board.place_piece(spaces.Piece.BEETLE, (-2, -4))  # White - bot's turn
        game_board.perform_action((board.HiveGameBoard.SKIP_TURN, None, None))  # Black - opponent's turn

        minimax_agent = agents.MinimaxAI(self.manager, max_depth=1, is_white=True)

        # Moving the beetle on top of the hive guarantees victory within 2 moves.
        action, eval = minimax_agent.get_action_selection_with_eval()
        print(f'Minimax depth 1 bot taking the following action: {action}; evaluation: {eval}')
        self.assertGreaterEqual(eval, minimax_agent.winning_value - 1 - 1)
        game_board.perform_action(action)  # White - bot's turn

        game_board.perform_action((board.HiveGameBoard.SKIP_TURN, None, None))  # Black - opponent's turn

        action, eval = minimax_agent.get_action_selection_with_eval()
        print(f'Minimax depth 1 bot taking the following action: {action}; evaluation: {eval}')
        self.assertGreaterEqual(eval, minimax_agent.winning_value)
        game_board.perform_action(action)  # White - bot's turn

        self.assertEqual(game_board.determine_winner(), board.HiveGameBoard.WHITE_WINNER)
        game_board.print_board(hex_board=False)

    def test_minimax_depth_2_find_win(self):
        game_board = self.manager.get_board()
        minimax_agent = agents.MinimaxAI(self.manager, max_depth=2, is_white=True)
        
        action, eval = minimax_agent.get_action_selection_with_eval()
        print(f'Minimax depth 2 bot taking the following action: {action}; evaluation: {eval}')
        self.assertGreaterEqual(eval, minimax_agent.winning_value - 2)
        game_board.perform_action(action)
        
        game_board.perform_action((board.HiveGameBoard.SKIP_TURN, None, None))

        action, eval = minimax_agent.get_action_selection_with_eval()
        print(f'Minimax depth 2 bot taking the following action: {action}; evaluation: {eval}')
        self.assertGreaterEqual(eval, minimax_agent.winning_value - 2)
        game_board.perform_action(action)
        
        game_board.perform_action((board.HiveGameBoard.SKIP_TURN, None, None))
        
        action, eval = minimax_agent.get_action_selection_with_eval()
        print(f'Minimax depth 2 bot taking the following action: {action}; evaluation: {eval}')
        self.assertGreaterEqual(eval, minimax_agent.winning_value)
        game_board.perform_action(action)
        
        self.assertEqual(game_board.determine_winner(), board.HiveGameBoard.WHITE_WINNER)
        game_board.print_board(hex_board=False)
