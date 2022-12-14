"""
This file is only used for debugging purposes and custom interactions with the game board and the AI.
This is not meant to be used other than for development purposes.
"""
import copy
from timeit import default_timer as timer

import random
import traceback
import src.game.board as board
import src.game.spaces as spaces
import src.agents as agents

import matplotlib.pyplot as plt


def test_sliding_rules():
    # This is copied from test/test_sliding_rules_no_mvt.py

    game_board = board.HiveGameBoard()

    # Making sure there are enough pieces to be placed for my test cases
    game_board.white_pieces_to_place = {
        'Ant': 5,
        'Queen Bee': 1,
        'Grasshopper': 5
    }
    game_board.black_pieces_to_place = {
        'Ant': 5,
        'Queen Bee': 1,
        'Grasshopper': 5
    }

    # Make moves for a sample game
    game_board.place_piece('Ant', (0, 0))  # White
    game_board.place_piece('Ant', (0, -1))  # Black
    game_board.place_piece('Ant', (-1, 0))  # White
    game_board.place_piece('Queen Bee', (0, -2))  # Black
    game_board.place_piece('Ant', (-2, 0))  # White
    game_board.place_piece('Ant', (1, -2))  # Black

    game_board.place_piece('Queen Bee', (-3, -1))  # White
    game_board.place_piece('Ant', (2, -2))  # Black
    game_board.place_piece('Grasshopper', (-3, -2))  # White
    game_board.place_piece('Grasshopper', (3, -1))  # Black
    game_board.place_piece('Grasshopper', (-3, -3))  # White
    game_board.place_piece('Grasshopper', (3, 0))  # Black
    game_board.place_piece('Grasshopper', (-2, -3))  # White

    game_board.print_board()
    print(game_board)

    print(f'Number of Empty Spaces on the game_board: {len(game_board.empty_spaces)}')

    for piece in game_board.pieces.values():
        if piece.name == spaces.Piece.ANT:
            print(f'Number of Empty Spaces Ant at {piece.location} can reach: {len(piece.possible_moves)}')

    print(f'Number of prevention sets: {len(game_board.ant_mvt_prevention_sets)}')

    game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (2, 0), piece_type=spaces.Piece.ANT)

    print('-' * 50)
    game_board.print_board()
    print('-' * 50)

    print(f'Number of Empty Spaces on the game_board: {len(game_board.empty_spaces)}')

    for piece in game_board.pieces.values():
        if piece.name == spaces.Piece.ANT:
            print(f'Number of Empty Spaces Ant at {piece.location} can reach: {len(piece.possible_moves)}')

    print(f'Number of prevention sets: {len(game_board.ant_mvt_prevention_sets)}')
    print('Prevention sets:')
    moveset = set(game_board.empty_spaces.keys())
    for prevention_set in game_board.ant_mvt_prevention_sets:
        print(prevention_set)
        moveset = moveset.difference(prevention_set)
    print('Free Empty Spaces Remaining:')
    print(moveset)

    print(f'Possible moves for Ant at (-2, 0): {game_board.pieces[(-2, 0)].possible_moves}')

    return game_board


def demo_game():
    move = board.HiveGameBoard.MOVE_PIECE
    place = board.HiveGameBoard.PLACE_PIECE

    ant = spaces.Piece.ANT
    beetle = spaces.Piece.BEETLE
    grasshopper = spaces.Piece.GRASSHOPPER
    queen_bee = spaces.Piece.QUEEN_BEE
    spider = spaces.Piece.SPIDER

    actions = [
        (place, (0, 0), grasshopper),
        (place, (0, 1), beetle),
        (place, (0, -1), ant),
        (place, (0, 2), queen_bee),
        (place, (1, 0), ant),
        (place, (0, 3), grasshopper),
        (place, (1, -1), queen_bee),
        (move, (0, 3), (0, -2)),
        (move, (1, 0), (0, 3)),
        (move, (0, -2), (2, 0)),
        (place, (-1, 3), spider),
        (place, (3, 0), beetle),
        (place, (1, 4), grasshopper),
        (move, (3, 0), (2, 0)),
        (move, (1, 4), (-1, 2)),
        (move, (2, 0), (1, -1)),
        (move, (-1, 3), (1, 3)),
        (place, (2, -1), ant),
        (place, (2, 4), grasshopper),
        (move, (2, -1), (2, 5)),
        (place, (2, 3), beetle),
        (place, (2, -1), ant),
        (move, (2, 3), (1, 2)),
        (place, (1, -2), grasshopper),
        (place, (-1, 3), spider),
        (move, (1, -2), (1, 0)),
        (move, (-1, 3), (-1, 1))
    ]

    game_board = board.HiveGameBoard()
    for action in actions:
        if game_board.determine_winner() is not None:
            break
        print(game_board.get_action_list())

        game_board.perform_action(action)
        game_board.print_board()

    print(f'The winner is: {game_board.determine_winner()}')


def check_for_errors(word_to_find=None, words_to_ignore=None, max_num_runs=25, max_actions=5000):
    num_runs = 0
    while num_runs < max_num_runs:
        try:
            board.BoardManager(new_manager=True)
            play_game(agents.RandomActionAI(), agents.RandomActionAI(), max_turns=max_actions, debug_output=True)
        except Exception:
            err_output = traceback.format_exc()
            if word_to_find is None and words_to_ignore is None:
                print(board.BoardManager().get_board())
                board.BoardManager().get_board().print_board()
                print(err_output)
                exit(1)
            if word_to_find is not None and word_to_find in err_output.lower():
                print(board.BoardManager().get_board())
                board.BoardManager().get_board().print_board()
                print(err_output)
                exit(1)
            if words_to_ignore is not None:
                found_word = False
                for word in words_to_ignore:
                    if word in err_output.lower():
                        found_word = True
                if not found_word:
                    print(board.BoardManager().get_board())
                    board.BoardManager().get_board().print_board()
                    print(err_output)
                    exit(1)

        num_runs += 1


def graph_data(evaluations_during_game, times_taken, num_actions_per_turn, player1, player2):
    # Plot the evaluation
    plt.figure(figsize=(10, 5))
    x_range = range(0, len(evaluations_during_game))
    plt.plot(x_range, evaluations_during_game)
    plt.xlabel('Turn Number')
    plt.ylabel('Evaluation')
    plt.title(f'Board Evaluation During a Hive Game\n'
              f'{player1} vs {player2}\n'
              f'Winner: {board.BoardManager().get_board().determine_winner()}')

    # Plot white data
    fig2, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    ax1.plot(x_range[::2], times_taken[::2], '#d2a200', alpha=0.75, label='White Time Taken')
    ax2.plot(x_range[::2], num_actions_per_turn[::2], 'gray', alpha=0.75, label='White Number of Actions')

    ax1.set_xlabel('Turn Number')
    ax1.set_ylabel('Time Taken [Seconds]')
    ax2.set_ylabel('Number of Actions')

    plt.title(f'{player1} Time Taken to Decide and Action During a Hive Game\n'
              f'{player1} vs {player2}\n'
              f'Winner: {board.BoardManager().get_board().determine_winner()}')
    fig2.legend()

    # Plot black data
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax4 = ax3.twinx()
    ax3.plot(x_range[1::2], times_taken[1::2], 'black', alpha=0.75, label='Black Time Taken')
    ax4.plot(x_range[1::2], num_actions_per_turn[1::2], 'gray', alpha=0.75, label='Black Number of Actions')

    ax3.set_xlabel('Turn Number')
    ax3.set_ylabel('Time Taken [Seconds]')
    ax4.set_ylabel('Number of Actions')
    fig3.legend()

    plt.title(f'{player2} Time Taken to Decide and Action During a Hive Game\n'
              f'{player1} vs {player2}\n'
              f'Winner: {board.BoardManager().get_board().determine_winner()}')

    plt.show()


def play_game(player1, player2, max_time=float("inf"), max_turns=float("inf"), graph_data_after_run=False,
              debug_output=False):
    board_manager = board.BoardManager()  # new_manager=True)

    if player1 == player2:
        player2 = copy.deepcopy(player1)

    player1.is_white = True
    player2.is_white = False

    evaluations_during_game = []
    times_taken = []
    num_actions_per_turn = []
    start_of_game = timer()

    try:
        while board_manager.get_board().determine_winner() is None and board_manager.get_board().turn_number < max_turns:
            time_check = timer()
            if time_check - start_of_game > max_time:
                break

            if not debug_output:
                board_manager.get_board().print_board()
                print(f'Current player: {"White" if board_manager.get_board().is_white_turn() else "Black"}')
                print(f'Evaluation: {board_manager.get_board().evaluate_state()}')
                print(f'Turn Number: {board_manager.get_board().turn_number}')

            start_of_action_decision = timer()
            if board_manager.get_board().is_white_turn():
                chosen_action = player1.get_action()
                agent_evaluation = player1.get_evaluation()
            else:
                chosen_action = player2.get_action()
                agent_evaluation = player2.get_evaluation()
            end_of_action_decision = timer()
            if not debug_output:
                print(f'Took {end_of_action_decision - start_of_action_decision} seconds to decide which action to take.')
            times_taken.append(end_of_action_decision - start_of_action_decision)
            num_actions_per_turn.append(len(board_manager.get_action_list()))

            evaluations_during_game.append(board_manager.get_board().evaluate_state())

            if not debug_output:
                perform_action_str = f'Agent eval before action: {agent_evaluation:0.2f} Performing action: {chosen_action}'
                print(perform_action_str)
                print('=' * len(perform_action_str))
            else:
                print(f'{chosen_action},')
            board_manager.perform_action(chosen_action)
    except KeyboardInterrupt:
        pass
    except Exception:
        board_manager.get_board().print_board(hex_board=False)
        board_manager.save_state('last_hive_error.hv')
        print(traceback.format_exc())

    if not debug_output:
        end_of_game = timer()

        board_manager.get_board().print_board()
        print(f'Winner: {board_manager.get_board().determine_winner()}')
        print(f'Total number of actions: {board_manager.get_board().turn_number}')
        print(f'Total game time: {end_of_game - start_of_game}')
        print(f'Average time per action: {(end_of_game - start_of_game)/board_manager.get_board().turn_number}')

        white_times_taken = times_taken[::2]
        black_times_taken = times_taken[1::2]

        print(f'Average Time Taken by White: {sum(white_times_taken) / len(white_times_taken)}')
        print(f'Average Time Taken by Black: {sum(black_times_taken) / len(black_times_taken)}')
        print()

        print('Number of actions for each object:')
        total_num_actions = 0
        for piece_type, action_times in board_manager.object_action_times.items():
            print(f'{piece_type:15} Total Number of Actions:   {len(action_times):n}')
            total_num_actions += len(action_times)

        print('Average times for each object action:')
        for piece_type, action_times in board_manager.object_action_times.items():
            print(f'{piece_type:15} Average Time:   {sum(action_times) / len(action_times):.6f}')

        print('Total times for each object action:')
        total_action_times = 0
        for piece_type, action_times in board_manager.object_action_times.items():
            print(f'{piece_type:15} Total Time:      {sum(action_times):.6f}')
            total_action_times += sum(action_times)

        print()
        print(f'Total number of actions:    {total_num_actions:n}')
        print(f'Average across all actions: {total_action_times/total_num_actions:.6f}')
        print(f'Total action times:         {total_action_times:.6f}')

        if board_manager.cloning_times:
            print(f'\nAverage time taken to undo an action: {sum(board_manager.cloning_times)/len(board_manager.cloning_times)}')
        print(f'Total time taken to undo actions: {sum(board_manager.cloning_times)}')

        print(f'\nAverage time taken to create an action list: '
              f'{sum(board_manager.getting_actions_times)/len(board_manager.getting_actions_times)}')
        print(f'Total time taken to create an action list: {sum(board_manager.getting_actions_times)}')

        if graph_data_after_run:
            graph_data(evaluations_during_game, times_taken, num_actions_per_turn, player1, player2)

        return evaluations_during_game, white_times_taken, black_times_taken, num_actions_per_turn, total_num_actions


def test_undo():
    game_board = test_sliding_rules()
    print('='*50)

    board_manager = board.BoardManager(new_manager=True)
    board_manager.current_board = game_board

    board_state2 = board_manager.get_successor((board.HiveGameBoard.PLACE_PIECE, (-3, 0), spaces.Piece.ANT))
    board_manager.get_board().print_board(hex_board=False)
    print(board_manager.get_board())

    board_manager.get_successor((board.HiveGameBoard.MOVE_PIECE, (2, 0), (-3, 1)))
    board_manager.get_board().print_board(hex_board=False)
    print(board_manager.get_board())

    board_state2.print_board(hex_board=False)

    board_manager.get_predecessor()
    board_manager.get_board().print_board(hex_board=False)
    print(board_manager.get_board())

    board_manager.get_successor((board.HiveGameBoard.MOVE_PIECE, (2, 0), (-4, 0)))
    board_manager.get_board().print_board(hex_board=False)
    print(board_manager.get_board())

    board_manager.get_predecessor()
    board_manager.get_board().print_board(hex_board=False)
    print(board_manager.get_board())

    board_manager.get_predecessor()
    board_manager.get_board().print_board(hex_board=False)
    print(board_manager.get_board())

    board_state2.print_board(hex_board=False)


def load_game(filename):
    manager = board.BoardManager(new_manager=True)
    manager.load_state(filename)
    manager.get_board().print_board(hex_board=False)


def make_sample_game():
    import src.game.pieces as pieces
    manager = board.BoardManager(new_manager=True)
    game_board = manager.get_board()

    pieces.Spider(game_board, 0, 0, True)
    pieces.QueenBee(game_board, 0, 1, False)
    pieces.Spider(game_board, 1, 2, False)
    pieces.Grasshopper(game_board, 1, 0, True)
    pieces.QueenBee(game_board, -1, -1, True)
    pieces.Ant(game_board, -1, 0, True)
    pieces.Beetle(game_board, -1, 0, False)
    pieces.Beetle(game_board, -2, 0, True)
    pieces.Ant(game_board, -3, 0, True)
    pieces.Spider(game_board, -4, -1, True)
    pieces.Grasshopper(game_board, -3, -1, False)
    pieces.Spider(game_board, -2, -1, False)
    pieces.Ant(game_board, -2, -2, False)
    pieces.Ant(game_board, 0, -1, False)
    pieces.Grasshopper(game_board, 0, -2, True)

    game_board.print_board()

    exit(0)


if __name__ == '__main__':
    # make_sample_game()
    # load_game('spider_error_game2.hv')
    # demo_game()
    # test_undo()
    # check_for_errors(max_num_runs=250, max_actions=1000)
    # exit(0)

    player = agents.Player()
    hex_player = agents.HexPlayer()
    random_ai = agents.RandomActionAI()
    best_next_move_ai = agents.BestNextMoveAI()
    minimax_ai1 = agents.MinimaxAI(max_depth=1)
    minimax_ai2 = agents.MinimaxAI(max_depth=2)
    minimax_ai3 = agents.MinimaxAI(max_depth=3, max_time=120)
    minimax_ai4 = agents.MinimaxAI(max_depth=4, max_time=10)
    minimax_ai8 = agents.MinimaxAI(max_depth=8, max_time=10)
    expectimax_ai1 = agents.ExpectimaxAI(max_depth=1, max_time=30)
    expectimax_ai2 = agents.ExpectimaxAI(max_depth=2, max_time=10)
    expectimax_ai3 = agents.ExpectimaxAI(max_depth=3, max_time=10)

    num_games = 1
    num_turns = 0
    num_white_wins = 0
    num_black_wins = 0
    num_draws = 0

    all_white_times_taken = []
    all_black_times_taken = []
    all_num_actions_per_turn = []
    actions_processed = []

    for i in range(num_games):
        # Run a game with specified players/AIs for white and black
        _, white_times, black_times, num_actions_per_turn, total_num_actions = play_game(
            hex_player,
            random_ai,
            graph_data_after_run=False,
            # max_turns=50,
        )

        game_board = board.BoardManager().get_board()
        if game_board.determine_winner() == board.HiveGameBoard.WHITE_WINNER:
            num_white_wins += 1
            all_white_times_taken += white_times
            all_black_times_taken += black_times
            all_num_actions_per_turn += num_actions_per_turn
            actions_processed.append(total_num_actions)
        elif game_board.determine_winner() == board.HiveGameBoard.BLACK_WINNER:
            num_black_wins += 1
            all_white_times_taken += white_times
            all_black_times_taken += black_times
            all_num_actions_per_turn += num_actions_per_turn
            actions_processed.append(total_num_actions)
        elif game_board.determine_winner() == board.HiveGameBoard.DRAW:
            num_draws += 1
            all_white_times_taken += white_times
            all_black_times_taken += black_times
            all_num_actions_per_turn += num_actions_per_turn
            actions_processed.append(total_num_actions)

        num_turns += game_board.turn_number

        print('='*50)
        print(f'\nResults after {i + 1} game{"s" if i != 0 else ""}:')
        print(f'White wins: {num_white_wins} / Black wins: {num_black_wins} / Draws: {num_draws}')
        print(f'Average number of turns per game: {num_turns/(i+1):.1f}\n')
        print()
        if all_white_times_taken and all_black_times_taken and all_num_actions_per_turn:
            print(f'Average time taken by White across all games: {sum(all_white_times_taken)/len(all_white_times_taken):0.6f}')
            print(f'Average time taken by Black across all games: {sum(all_black_times_taken)/len(all_black_times_taken):0.6f}')
            print(f'Average number of actions on a turn: {sum(all_num_actions_per_turn)/len(all_num_actions_per_turn):.0f}')
            print(f'Average number of actions processed in a game: {sum(actions_processed)/num_games:.0f}')
        print('='*50)

        board.BoardManager(new_manager=True)
