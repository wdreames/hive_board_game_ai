"""
William Reames
CNU Computer Science Capstone
AI for the Hive Board Game
2022
"""
import random
import traceback
import src.game.board as board
import src.game.spaces as spaces


def play_game():
    # Initialize the game board
    game_board = board.HiveGameBoard()

    while game_board.determine_winner() is None:
        print('-' * 50)
        print(game_board)
        game_board.print_board()

        if game_board.is_white_turn():
            current_player = 'white'
        else:
            current_player = 'black'
        print('Game turn: {}\nPlayer to Move: {}\nPlayer Turn: {}\n'.format(game_board.turn_number, current_player,
                                                                            (game_board.turn_number + 1) // 2))

        pieces_to_play, locations_to_place, possible_moves = game_board.get_all_possible_actions()

        print('{} has the following pieces to play: {}'.format(current_player, pieces_to_play))
        print('{} has the following locations to place a piece: {}'.format(current_player, locations_to_place))
        print('{} has the following pieces to move: {}'.format(current_player, set(possible_moves.keys())))

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
                    game_board.place_piece(piece_input, (x_val, y_val))
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

                    game_board.move_piece((x_val, y_val), (x_val2, y_val2))
                else:
                    print('Invalid selection. Please select from the list of available pieces to move')

        # except KeyError:
        #     print('Error in processing input: ', traceback.format_exc())
        except ValueError:
            print('Invalid input: ', traceback.format_exc())

    print('Winner: {}'.format(game_board.determine_winner()))


def play_game_with_manager():
    board_manager = board.BoardManager()

    actions_performed = []
    while board_manager.get_board().determine_winner() is None:
        current_board = board_manager.get_board()
        current_board.print_board()
        print(f'Current player: {"White" if current_board.is_white_turn() else "Black"}')
        print(f'White Pieces that can move: {set(current_board.white_possible_moves.keys())}')
        print(f'Black Pieces that can move: {set(current_board.black_possible_moves.keys())}')
        print(f'Evaluation: {current_board.evaluate_state()}')
        print(f'Turn Number: {current_board.turn_number}')
        print('-' * 25)
        actions = board_manager.get_action_list()
        randIndex = random.randint(0, len(actions) - 1)
        actions_performed.append(actions[randIndex])
        board_manager.perform_action(actions[randIndex])

    board_manager.get_board().print_board()
    print(actions_performed)
    print(f'Total number of actions: {board_manager.get_board().turn_number}')


def test_successive_states():
    board_manager = board.BoardManager()

    current_state = board_manager.get_board()
    current_state.print_board()
    for action in current_state.get_action_list():
        successive_state = board_manager.get_successor(current_state, action)
        print(successive_state)
        successive_state.print_board()
        for successive_action in successive_state.get_action_list():
            successive_state2 = board_manager.get_successor(successive_state, successive_action)
            print(successive_state2)
            successive_state2.print_board()
        break
    current_state.print_board()


def test_game1():
    game_board = board.HiveGameBoard()
    # game_board.place_piece(spcs.Piece.ANT, (0, 0))
    # game_board.print_board()
    # game_board.place_piece(spcs.Piece.QUEEN_BEE, (-1, 0))
    # game_board.print_board()
    # game_board.place_piece(spcs.Piece.ANT, (1, 1))
    # game_board.print_board()
    # print(game_board)
    # print(game_board.pieces[(-1, 0)])
    # print(game_board.pieces[(0, 0)])
    # game_board.move_piece((-1, 0), (0, 1))
    # game_board.print_board()
    # print(game_board)
    #
    # print('-' * 50)
    # print(game_board.pieces[(0, 1)])

    PLACE = board.HiveGameBoard.PLACE_PIECE
    MOVE = board.HiveGameBoard.MOVE_PIECE

    game_board.perform_action_helper(PLACE, (0, 0), piece_type=spaces.Piece.BEETLE)
    print(game_board)
    game_board.print_board()

    game_board.perform_action_helper(PLACE, (-1, -1), piece_type=spaces.Piece.ANT)
    print(game_board)
    game_board.print_board()

    game_board.perform_action_helper(MOVE, (0, 0), new_location=(-1, -1))

    print(game_board)
    game_board.print_board()
    print(board.HiveGameBoard().empty_spaces[(0, 0)])
    print(board.HiveGameBoard().empty_spaces[(-1, 0)])


def test_game2():
    game_board = board.HiveGameBoard()
    PLACE = board.HiveGameBoard.PLACE_PIECE
    MOVE = board.HiveGameBoard.MOVE_PIECE

    game_board.perform_action_helper(PLACE, (0, 0), piece_type=spaces.Piece.ANT)
    game_board.print_board()
    game_board.perform_action_helper(PLACE, (0, 1), piece_type=spaces.Piece.BEETLE)
    game_board.print_board()
    game_board.perform_action_helper(PLACE, (0, -1), piece_type=spaces.Piece.QUEEN_BEE)
    game_board.print_board()
    game_board.perform_action_helper(MOVE, (0, 1), new_location=(0, 0))
    game_board.print_board()
    game_board.perform_action_helper(MOVE, (0, -1), new_location=(-1, -1))
    game_board.print_board()
    game_board.perform_action_helper(MOVE, (0, 0), new_location=(-1, -1))
    game_board.print_board()
    game_board.perform_action_helper(PLACE, (0, 1), piece_type=spaces.Piece.ANT)
    game_board.print_board()
    game_board.perform_action_helper(PLACE, (-2, -2), piece_type=spaces.Piece.QUEEN_BEE)
    game_board.print_board()
    game_board.perform_action_helper(PLACE, (0, 2), piece_type=spaces.Piece.GRASSHOPPER)
    game_board.print_board()
    game_board.perform_action_helper(PLACE, (-1, -2), piece_type=spaces.Piece.ANT)
    game_board.print_board()
    game_board.perform_action_helper(PLACE, (0, 3), piece_type=spaces.Piece.GRASSHOPPER)
    game_board.print_board()
    game_board.perform_action_helper(PLACE, (-2, -1), piece_type=spaces.Piece.BEETLE)
    game_board.print_board()
    game_board.perform_action_helper(PLACE, (0, 4), piece_type=spaces.Piece.ANT)
    game_board.print_board()
    game_board.perform_action_helper(MOVE, (-2, -1), new_location=(-1, -1))
    game_board.print_board()
    game_board.perform_action_helper(MOVE, (0, 2), new_location=(0, -1))
    game_board.print_board()

    print(game_board)
    print(game_board.pieces[(0, -1)])
    print(game_board.pieces[(0, 3)])


def test_game3():
    game_board = board.HiveGameBoard()
    PLACE = board.HiveGameBoard.PLACE_PIECE
    MOVE = board.HiveGameBoard.MOVE_PIECE

    game_board.perform_action_helper(PLACE, (0, 0), piece_type=spaces.Piece.GRASSHOPPER)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(PLACE, (1, 0), piece_type=spaces.Piece.GRASSHOPPER)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(PLACE, (-1, 0), piece_type=spaces.Piece.ANT)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(MOVE, (1, 0), new_location=(-2, 0))
    game_board.print_board()
    print('-' * 10)

    print(game_board)
    # print(game_board.pieces[(0, 0)])
    # print(game_board.pieces[(1, 0)])
    # print(game_board.pieces[(-1, 0)])


def test_game4():
    game_board = board.HiveGameBoard()
    PLACE = board.HiveGameBoard.PLACE_PIECE
    MOVE = board.HiveGameBoard.MOVE_PIECE

    game_board.perform_action_helper(PLACE, (0, 0), piece_type=spaces.Piece.BEETLE)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(PLACE, (1, 0), piece_type=spaces.Piece.GRASSHOPPER)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(PLACE, (-1, -1), piece_type=spaces.Piece.SPIDER)
    game_board.print_board()
    print('-' * 10)
    print(game_board)
    game_board.perform_action_helper(PLACE, (2, 0), piece_type=spaces.Piece.SPIDER)
    game_board.print_board()
    print('-' * 10)
    print(game_board)
    game_board.perform_action_helper(MOVE, (-1, -1), new_location=(2, -1))
    print(game_board)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(PLACE, (3, 1), piece_type=spaces.Piece.GRASSHOPPER)
    print(game_board)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(PLACE, (-1, 0), piece_type=spaces.Piece.QUEEN_BEE)
    print(game_board)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(MOVE, (3, 1), new_location=(1, -1))
    print(game_board)
    game_board.print_board()
    print('-' * 10)


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

    print(f'Number of Empty Spaces on the board: {len(game_board.empty_spaces)}')

    for piece in game_board.pieces.values():
        if piece.name == spaces.Piece.ANT:
            print(f'Number of Empty Spaces Ant at {piece.location} can reach: {len(piece.possible_moves)}')

    print(f'Number of prevention sets: {len(game_board.ant_mvt_prevention_sets)}')

    game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (2, 0), piece_type=spaces.Piece.ANT)

    print('-' * 50)
    game_board.print_board()
    print('-' * 50)

    print(f'Number of Empty Spaces on the board: {len(game_board.empty_spaces)}')

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


def test_game5():
    game_board = test_sliding_rules()
    game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (-3, 0), piece_type=spaces.Piece.ANT)
    print(game_board)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (2, 0), new_location=(1, 0))
    print(game_board)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(board.HiveGameBoard.MOVE_PIECE, (-3, 0), new_location=(-1, -3))
    print(game_board)
    game_board.print_board()
    print('-' * 10)
    game_board.perform_action_helper(board.HiveGameBoard.PLACE_PIECE, (2, 0), piece_type=spaces.Piece.ANT)
    print(game_board)
    game_board.print_board()
    print('-' * 10)


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


if __name__ == '__main__':
    # test_sliding_rules()
    # demo_game()
    play_game_with_manager()
    # test_successive_states()
    # test_game5()
