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
from src.game_board.piece import Piece


def play_game():
    # Initialize the game board
    board = HiveGameBoard()

    while board.determine_winner() is None:
        print('-' * 50)
        print(board)
        board.print_board()

        if board.is_white_turn():
            current_player = 'white'
        else:
            current_player = 'black'
        print('Game turn: {}, Player to Move: {}, Player Turn: {}'.format(board.turn_number, current_player,
                                                                          (board.turn_number + 1) // 2))

        pieces_to_play, locations_to_place, possible_moves = board.get_all_possible_actions()

        print('{} has the following pieces to play: {}'.format(current_player, pieces_to_play))
        print('{} has the following locations to place a piece: {}'.format(current_player, locations_to_place))
        print('{} has the following pieces on the board: {}'.format(current_player, set(possible_moves.keys())))

        try:
            # TODO: [UI] Assuming properly formatted input for now
            place_or_move = input('Do you want to place a piece (1) or move a piece (2)?')
            if int(place_or_move) == 1:
                piece_input = input('Which piece would you like to play?')
                location_input = input('Where would you like to place the piece?')
                location_input = location_input.split(',')
                x_val = int(location_input[0][1:])
                y_val = int(location_input[1][:-1])

                if (x_val, y_val) in locations_to_place:
                    print('placing {} at ({}, {})'.format(piece_input, x_val, y_val))
                    board.place_piece(piece_input, (x_val, y_val))
                else:
                    print('Invalid location. Please select from the list of available locations to place a piece')
            else:
                piece_loc_input = input('Which piece would you like to move (enter location)?')
                piece_loc_input = piece_loc_input.split(',')
                x_val = int(piece_loc_input[0][1:])
                y_val = int(piece_loc_input[1][:-1])
                if (x_val, y_val) in possible_moves:
                    print('{} has the following possible moves: {}'.format((x_val, y_val),
                                                                           possible_moves[(x_val, y_val)]))
                    move_location_input = input('Where would you like to move the piece?')
                    move_location_input = move_location_input.split(',')
                    x_val2 = int(move_location_input[0][1:])
                    y_val2 = int(move_location_input[1][:-1])

                    board.move_piece((x_val, y_val), (x_val2, y_val2))
                else:
                    print('Invalid selection. Please select from the list of available pieces to move')

        except KeyError:
            print('Error in processing input: ', traceback.format_exc())

    print('Winner: {}'.format(board.determine_winner()))


def test_game():
    board = HiveGameBoard()
    board.place_piece(Piece.ANT, (0, 0))
    board.print_board()
    board.place_piece(Piece.QUEEN_BEE, (-1, 0))
    board.print_board()
    board.place_piece(Piece.ANT, (1, 1))
    board.print_board()
    print(board)
    print(board.pieces[(-1, 0)])
    print(board.pieces[(0, 0)])
    board.move_piece((-1, 0), (0, 1))
    board.print_board()
    print(board)

    print('-' * 50)
    print(board.pieces[(0, 1)])


# TODO: [UI] Make this nicer later on
if __name__ == '__main__':
    test_game()
