"""
William Reames
CNU Computer Science Capstone
AI for the Hive Board Game
2022
"""
# TODO: [Formatting] Refactor imports across all files. Import system feels inconsistent across files
# TODO: [Formatting] Add comments for all classes and methods
import traceback
from src.game_board.board import HiveGameBoard

# TODO: [UI] Make this nicer later on
if __name__ == '__main__':
    # Initialize the game board
    board = HiveGameBoard()

    while board.determine_winner() is None:
        print('-' * 50)
        # print(board)
        board.print_board()

        if board.is_white_turn():
            current_player = 'white'
        else:
            current_player = 'black'
        print('Game turn: {}, Player to Move: {}, Player Turn: {}'.format(board.turn_number, current_player,
                                                                          (board.turn_number + 1) // 2))

        pieces_to_play, locations_to_place = board.get_all_possible_actions()

        print('{} has the following pieces to play: {}'.format(current_player, pieces_to_play))
        print('{} has the following locations to place a piece: {}'.format(current_player, locations_to_place))

        try:
            # TODO: [UI] Assuming properly formatted input for now
            piece_input = input('Which piece would you like to play?')
            location_input = input('Where would you like to place the piece')
            location_input = location_input.split(',')
            x_val = int(location_input[0][1:])
            y_val = int(location_input[1][:-1])
            print('placing {} at ({}, {})'.format(piece_input, x_val, y_val))

            board.place_piece(piece_input, (x_val, y_val))
        except KeyError:
            print('Error in processing input: ', traceback.format_exc())

    print('Winner: {}'.format(board.determine_winner()))
