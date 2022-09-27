"""
William Reames
CNU Computer Science Capstone
AI for the Hive Board Game
2022
"""
# TODO: [Formatting] Add comments for all classes and methods
import traceback
import src.game.board as brd
import src.game.spaces as spcs


def play_game():
    # Initialize the game board
    board = brd.HiveGameBoard()

    while board.determine_winner() is None:
        print('-' * 50)
        print(board)
        board.print_board()

        if board.is_white_turn():
            current_player = 'white'
        else:
            current_player = 'black'
        print('Game turn: {}\nPlayer to Move: {}\nPlayer Turn: {}\n'.format(board.turn_number, current_player,
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

        # except KeyError:
        #     print('Error in processing input: ', traceback.format_exc())
        except ValueError:
            print('Invalid input: ', traceback.format_exc())

    print('Winner: {}'.format(board.determine_winner()))


def test_game1():
    board = brd.HiveGameBoard(new_board=True)
    # board.place_piece(spcs.Piece.ANT, (0, 0))
    # board.print_board()
    # board.place_piece(spcs.Piece.QUEEN_BEE, (-1, 0))
    # board.print_board()
    # board.place_piece(spcs.Piece.ANT, (1, 1))
    # board.print_board()
    # print(board)
    # print(board.pieces[(-1, 0)])
    # print(board.pieces[(0, 0)])
    # board.move_piece((-1, 0), (0, 1))
    # board.print_board()
    # print(board)
    #
    # print('-' * 50)
    # print(board.pieces[(0, 1)])

    PLACE = brd.HiveGameBoard.PLACE_PIECE
    MOVE = brd.HiveGameBoard.MOVE_PIECE

    board.perform_action(PLACE, (0, 0), piece_type=spcs.spcs.Piece.BEETLE)
    print(board)
    board.print_board()

    board.perform_action(PLACE, (-1, -1), piece_type=spcs.spcs.Piece.ANT)
    print(board)
    board.print_board()

    board.perform_action(MOVE, (0, 0), new_location=(-1, -1))

    print(board)
    board.print_board()
    print(brd.HiveGameBoard().empty_spaces[(0, 0)])
    print(brd.HiveGameBoard().empty_spaces[(-1, 0)])


def test_game2():
    board = brd.HiveGameBoard(new_board=True)
    PLACE = brd.HiveGameBoard.PLACE_PIECE
    MOVE = brd.HiveGameBoard.MOVE_PIECE

    board.perform_action(PLACE, (0, 0), piece_type=spcs.Piece.ANT)
    board.print_board()
    board.perform_action(PLACE, (0, 1), piece_type=spcs.Piece.BEETLE)
    board.print_board()
    board.perform_action(PLACE, (0, -1), piece_type=spcs.Piece.QUEEN_BEE)
    board.print_board()
    board.perform_action(MOVE, (0, 1), new_location=(0, 0))
    board.print_board()
    board.perform_action(MOVE, (0, -1), new_location=(-1, -1))
    board.print_board()
    board.perform_action(MOVE, (0, 0), new_location=(-1, -1))
    board.print_board()
    board.perform_action(PLACE, (0, 1), piece_type=spcs.Piece.ANT)
    board.print_board()
    board.perform_action(PLACE, (-2, -2), piece_type=spcs.Piece.QUEEN_BEE)
    board.print_board()
    board.perform_action(PLACE, (0, 2), piece_type=spcs.Piece.GRASSHOPPER)
    board.print_board()
    board.perform_action(PLACE, (-1, -2), piece_type=spcs.Piece.ANT)
    board.print_board()
    board.perform_action(PLACE, (0, 3), piece_type=spcs.Piece.GRASSHOPPER)
    board.print_board()
    board.perform_action(PLACE, (-2, -1), piece_type=spcs.Piece.BEETLE)
    board.print_board()
    board.perform_action(PLACE, (0, 4), piece_type=spcs.Piece.ANT)
    board.print_board()
    board.perform_action(MOVE, (-2, -1), new_location=(-1, -1))
    board.print_board()
    board.perform_action(MOVE, (0, 2), new_location=(0, -1))
    board.print_board()

    print(board)
    print(board.pieces[(0, -1)])
    print(board.pieces[(0, 3)])

    play_game()


def test_game3():
    board = brd.HiveGameBoard(new_board=True)
    PLACE = brd.HiveGameBoard.PLACE_PIECE
    MOVE = brd.HiveGameBoard.MOVE_PIECE

    board.perform_action(PLACE, (0, 0), piece_type=spcs.Piece.GRASSHOPPER)
    board.print_board()
    print('-' * 10)
    board.perform_action(PLACE, (1, 0), piece_type=spcs.Piece.GRASSHOPPER)
    board.print_board()
    print('-' * 10)
    board.perform_action(PLACE, (-1, 0), piece_type=spcs.Piece.ANT)
    board.print_board()
    print('-' * 10)
    board.perform_action(MOVE, (1, 0), new_location=(-2, 0))
    board.print_board()
    print('-' * 10)

    print(board)
    # print(board.pieces[(0, 0)])
    # print(board.pieces[(1, 0)])
    # print(board.pieces[(-1, 0)])

    # play_game()


def test_game4():
    board = brd.HiveGameBoard(new_board=True)
    PLACE = brd.HiveGameBoard.PLACE_PIECE
    MOVE = brd.HiveGameBoard.MOVE_PIECE

    board.perform_action(PLACE, (0, 0), piece_type=spcs.Piece.BEETLE)
    board.print_board()
    print('-' * 10)
    board.perform_action(PLACE, (1, 0), piece_type=spcs.Piece.GRASSHOPPER)
    board.print_board()
    print('-' * 10)
    board.perform_action(PLACE, (-1, -1), piece_type=spcs.Piece.SPIDER)
    board.print_board()
    print('-' * 10)
    board.perform_action(PLACE, (2, 0), piece_type=spcs.Piece.SPIDER)
    board.print_board()
    print('-' * 10)
    board.perform_action(MOVE, (-1, -1), new_location=(2, -1))
    print(board)
    board.print_board()
    print('-' * 10)
    board.perform_action(PLACE, (3, 1), piece_type=spcs.Piece.GRASSHOPPER)
    print(board)
    board.print_board()
    print('-' * 10)
    board.perform_action(PLACE, (-1, 0), piece_type=spcs.Piece.QUEEN_BEE)
    print(board)
    board.print_board()
    print('-' * 10)
    board.perform_action(MOVE, (3, 1), new_location=(1, -1))
    print(board)
    board.print_board()
    print('-' * 10)


    # print(board)
    #
    # print(board.pieces[(2, 0)])
    # print(board.pieces[(2, -1)])
    # print(board.pieces[(-1, -1)])
    # print(board.empty_spaces[(2, -1)])

    # play_game()


# TODO: [UI] Make this nicer later on
if __name__ == '__main__':
    # play_game()
    # test_game1()
    # test_game2()
    # test_game3()
    test_game4()
    # play_game()
