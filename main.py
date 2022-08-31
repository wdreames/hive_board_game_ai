"""
William Reames
CNU Computer Science Capstone
AI for the Hive Board Game
2022
"""
# TODO: [Formatting] Refactor imports across all files. Import system feels inconsistent across files
# TODO: [Formatting] Add comments for all classes and methods
from game_board.board import HiveGameBoard
from game_board.empty_space import EmptySpace
from game_board.pieces.ant import Ant
from game_board.pieces.queen_bee import QueenBee
from game_board.pieces.grasshopper import Grasshopper

if __name__ == '__main__':
    # Initialize the game board
    board = HiveGameBoard()

    while board.determine_winner() is None:
        print('-' * 50)
        print(board)

        if board.is_white_turn():
            current_player = 'white'
        else:
            current_player = 'black'
        print('Game turn: {}, Player to Move: {}, Player Turn: {}'.format(board.turn_number, current_player,
                                                                          (board.turn_number + 1) // 2))

        pieces_to_play, locations_to_place = HiveGameBoard().get_all_possible_actions()

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

            HiveGameBoard().place_piece(piece_input, (x_val, y_val))
        except KeyError as exception:
            print('Error in processing input: ', exception)

    # TODO: [UI] Implementation after winner has been determined
