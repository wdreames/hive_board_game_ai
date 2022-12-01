import argparse
import copy
import random
import traceback
import src.game.board as board
import src.agents as agents
import src.utils as utils


custom_depth = None


def set_player_arguments():
    arguments = parse_arguments()

    if arguments['load']:
        board.BoardManager().load_state(arguments['load'])
    if arguments['size']:
        # TODO: Add a way to change board size
        pass
    if arguments['depth']:
        pass

    return arguments


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l',
        '--load',
        help='Load a previously saved game from the `data` folder'
    )
    parser.add_argument(
        "-s",
        "--size",
        help="Enter a maximum board size as an integer value. Default is 12",
        type=int,
        default=12
    )
    parser.add_argument(
        "-d",
        "--depth",
        help=
        """
        Enter the maximum depth the AI can search as an integer value. This is equivalent to how many turns in
        the future the AI will check. For reference, the easy AI looks 0 moves in the future, the medium AI
        looks 1 move in the future, and the hard AI looks 2 moves in the future. It should be noted, though, that
        searching a single extra turn in the future increases the time the AI takes to think exponentially.
        """,
        type=int
    )

    args = parser.parse_args()

    return {'load': args.load, 'size': args.size, 'depth': args.depth}


def play_game(player1, player2):
    board_manager = board.BoardManager()

    if player1 == player2:
        player2 = copy.deepcopy(player1)

    player1.is_white = True
    player2.is_white = False

    try:
        while board_manager.get_board().determine_winner() is None:

            board_manager.get_board().print_board()
            print(f'Current player: {"White" if board_manager.get_board().is_white_turn() else "Black"}')
            print(f'Turn Number: {board_manager.get_board().turn_number}')

            if board_manager.get_board().is_white_turn():
                chosen_action = player1.get_action()
            else:
                chosen_action = player2.get_action()

            board_manager.perform_action(chosen_action)
    except KeyboardInterrupt:
        pass
    except Exception:
        board_manager.get_board().print_board(hex_board=False)
        print(traceback.format_exc())

    board_manager.get_board().print_board()
    print(f'Winner: {board_manager.get_board().determine_winner()}')


if __name__ == '__main__':
    arguments = set_player_arguments()
    player = agents.HexPlayer()

    play_against_player = 'Another player'
    play_against_random = 'A random AI'
    play_against_easy = 'An easy AI'
    play_against_medium = 'A medium AI'
    play_against_hard = 'A hard AI'

    if not arguments['depth']:
        opponent_selection = utils.make_choice(
            'Choose your opponent.',
            'Select from the following options:',
            [
                play_against_player,
                play_against_random,
                play_against_easy,
                play_against_medium,
                play_against_hard,
            ]
        )
        print()
    else:
        opponent_selection = arguments['depth']

    if opponent_selection == play_against_player:
        opponent = agents.HexPlayer()
    elif opponent_selection == play_against_random:
        opponent = agents.RandomActionAI()
    elif opponent_selection == play_against_easy:
        opponent = agents.BestNextMoveAI()
    elif opponent_selection == play_against_medium:
        opponent = agents.MinimaxAI(max_depth=1)
    else:
        if arguments['depth']:
            print(f'Using an AI with depth {arguments["depth"]}.\n')

        max_time = None
        while max_time is None:
            print(f'The AI can sometimes take a long time to think.')
            print('However, you can set a limit to the amount of time it has to think by entering a maximum wait time'
                  ' in seconds. Press enter to play with an unlimited thinking time.')
            max_time_str = input('Please enter an integer number for the number of seconds the AI can think:')
            if not max_time_str:
                max_time = float('inf')
            else:
                if max_time_str.isdigit():
                    max_time = int(max_time_str)
                else:
                    print('Error. You did not enter an integer value. Please try again.')

        max_depth = arguments['depth'] if arguments['depth'] else 2
        opponent = agents.MinimaxAI(max_depth=max_depth, max_time=max_time)

    white = 'White'
    black = 'Black'
    random_color = 'Random Selection'
    color_selection = utils.make_choice(
        'Would you like to play as White or Black?',
        'Select an option:',
        [white, black, random_color]
    )

    if color_selection == random_color:
        color_selection = random.choice([white, black])

    if color_selection == white:
        play_game(player, opponent)
    else:
        play_game(opponent, player)
