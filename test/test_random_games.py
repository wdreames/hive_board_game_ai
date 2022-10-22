from timeit import default_timer as timer

import src.game.board as board
import src.game.spaces as spaces
import random
import traceback
import unittest


class TestRandomGames(unittest.TestCase):
    """
    This test case runs a series of 10 games with randomly chosen moves, with a maximum of 5000 moves per game.
    The test passes if no errors occurr during runtime.
    """

    def test_random_games(self):
        total_actions = 0
        total_time = 0

        number_of_games = 10
        successful_games = 0
        for i in range(number_of_games):
            action_to_perform = None

            start_of_run = timer()
            board_manager = board.BoardManager(new_manager=True)
            board_manager.get_board().white_pieces_to_place[spaces.Piece.GRASSHOPPER] = 0
            # board_manager.get_board().white_pieces_to_place[spaces.Piece.SPIDER] = 0
            board_manager.get_board().black_pieces_to_place[spaces.Piece.GRASSHOPPER] = 0
            # board_manager.get_board().black_pieces_to_place[spaces.Piece.SPIDER] = 0
            try:
                while board_manager.get_board().determine_winner() is None and board_manager.get_board().turn_number < 5000:
                    actions = board_manager.get_action_list()
                    rand_index = random.randint(0, len(actions) - 1)
                    action_to_perform = actions[rand_index]
                    board_manager.perform_action(action_to_perform)
            except Exception:
                print('=' * 50)
                print('An error has occurred!')
                print(traceback.format_exc())
                print()
                print(f'Action performed: {action_to_perform}')
                print('Board details:')
                board_manager.get_board().print_board()
                print(board_manager)
                print('=' * 50)
                continue

            end_of_run = timer()

            total_actions += board_manager.get_board().turn_number
            total_time += end_of_run - start_of_run
            print(f'Completed game {i+1}. Performed {board_manager.get_board().turn_number} moves in '
                  f'{end_of_run - start_of_run} seconds.')
            successful_games += 1

        print(f'Total number of actions:    {total_actions}')
        print(f'Total time taken:           {total_time}')
        print(f'Average time per action:    {total_time/total_actions}')

        self.assertEqual(number_of_games, successful_games,
                         f'{number_of_games - successful_games} errors occurred over the course of '
                         f'{number_of_games} games')


if __name__ == '__main__':
    unittest.main()
