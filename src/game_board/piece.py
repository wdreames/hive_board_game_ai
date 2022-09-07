import src.game_board.board as board
import src.game_board.empty_space as emt

from abc import abstractmethod
from src.game_board.hex_space import HexSpace


class Piece(HexSpace):
    """
    Used to represent a piece on the game board. This is an abstract class.
    Superclass for Ant, Grasshopper, and QueenBee.
    """

    def __init__(self, x=0, y=0, is_white=True):
        """
        Create a new piece.

        :param x: int
            x location
        :param y: int
            y location
        :param is_white: boolean
            True if this piece belongs to White; False if this piece belongs to Black
        """
        super().__init__(x, y)
        self.is_white = is_white
        self.possible_moves = set()
        self.preventing_sliding_for = {}

        # TODO: [Efficiency] There are some redundant actions here to reduce the amount of written code
        board.HiveGameBoard().pieces[self.location] = self
        self.move_to(self.location)

    # TODO: [Formatting] Reformat this function for added readability
    def move_to(self, new_location):
        """
        Moves this piece to a new location. This also updates any previous/new connections to other pieces. No movement
        will happen if the move is invalid.

        :param new_location: tuple
            (x, y) location where the piece will be placed
        """
        # TODO: [Movement] Also need to ensure it's in the list of moves
        if new_location not in board.HiveGameBoard().empty_spaces:
            print('Error: No empty space at {} to place a piece'.format(new_location))
            # TODO: [UI] Raise an actual error
            return

        # TODO: [Movement] Unlock & disconnect from any relevant pieces that used to be connected
        #       Also need to see if any cannot_move_to sets need to be updated

        # Move this piece in the board dictionary
        board.HiveGameBoard().pieces.pop(self.location)
        old_location = self.location
        self.location = new_location
        board.HiveGameBoard().pieces[new_location] = self

        # Copy the connections from the empty space at the new location
        related_empty_space = board.HiveGameBoard().empty_spaces[new_location]
        self.connected_pieces = related_empty_space.connected_pieces
        self.connected_empty_spaces = related_empty_space.connected_empty_spaces

        # Update all the piece and empty space connections
        all_connected_spaces = self.connected_empty_spaces.union(self.connected_pieces)
        for space_location in all_connected_spaces:
            board.HiveGameBoard().get_all_spaces()[space_location].add_connection_to_piece(self.location)

        if len(self.connected_pieces) == 1:
            board.HiveGameBoard().pieces[list(self.connected_pieces)[0]].lock()

        # Delete the empty space at this location
        related_empty_space.remove()

        self._create_surrounding_emt_spcs()

        # Check if any cannot_slide_to sets need to be updated
        self._update_sliding()

    def _create_surrounding_emt_spcs(self):
        # Helper function for move_to(location)
        # Add new empty spaces
        all_connected_spaces = self.connected_empty_spaces.union(self.connected_pieces)
        surrounding_locations = {(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x - 1, self.y),
                                 (self.x + 1, self.y),
                                 (self.x, self.y + 1), (self.x + 1, self.y + 1)}
        locations_for_new_empty_spaces = surrounding_locations.difference(all_connected_spaces)

        for point in locations_for_new_empty_spaces:
            emt.EmptySpace(point[0], point[1])

    # TODO: [Movement] Not fully functional... see notebook
    #       Oh an I also need to set this pieces' cannot_slide to values...
    #       Idk if that's something that is already implemented with the current algorithm
    def _update_sliding(self):
        # Helper function for move_to(location)
        x = self.x
        y = self.y
        self._check_if_preventing_sliding((x - 2, y - 1), (x - 1, y - 1), (x - 1, y))
        self._check_if_preventing_sliding((x - 1, y + 1), (x - 1, y), (x, y + 1))
        self._check_if_preventing_sliding((x + 1, y + 2), (x, y + 1), (x + 1, y + 1))
        self._check_if_preventing_sliding((x + 2, y + 1), (x + 1, y + 1), (x + 1, y))
        self._check_if_preventing_sliding((x + 1, y - 1), (x + 1, y), (x, y - 1))
        self._check_if_preventing_sliding((x - 1, y - 2), (x, y - 1), (x - 1, y - 1))

    def _check_if_preventing_sliding(self, other_piece_loc, space1_loc, space2_loc):
        # Helper function
        # Spaces at (location1) and (location2) cannot slide to each other
        game_board = board.HiveGameBoard()
        if other_piece_loc in board.HiveGameBoard().pieces:
            all_spaces = game_board.get_all_spaces()

            other_piece = game_board.pieces[other_piece_loc]
            space1 = all_spaces[space1_loc]
            space2 = all_spaces[space2_loc]

            self._helper_add_to_dict_set(self.preventing_sliding_for, space1_loc, space2_loc)
            self._helper_add_to_dict_set(other_piece.preventing_sliding_for, space1_loc, space2_loc)

            self._helper_add_to_dict_set(self.preventing_sliding_for, space2_loc, space1_loc)
            self._helper_add_to_dict_set(other_piece.preventing_sliding_for, space2_loc, space1_loc)

            self._helper_add_to_dict_set(space1.sliding_prevented_to, space2_loc, self.location)
            self._helper_add_to_dict_set(space1.sliding_prevented_to, space2_loc, other_piece_loc)
            self._helper_add_to_dict_set(space2.sliding_prevented_to, space1_loc, self.location)
            self._helper_add_to_dict_set(space2.sliding_prevented_to, space1_loc, other_piece_loc)

    # TODO: [Formatting] Put this function into a utils class
    @staticmethod
    def _helper_add_to_dict_set(dictionary, key, value):
        if key in dictionary:
            dictionary[key].add(value)
        else:
            dictionary[key] = {value}

    # def formed_loop(self):
    #     # Check if two pieces are on opposite sides after being placed w/ 1+ empty spaces in between
    #     return False

    # TODO: [Movement] Implement lock method; currently have a placeholder for testing
    def lock(self):
        """
        Called when the piece is put into a position where it can no longer move. This function clears the set of
        all possible moves
        """
        self.possible_moves.clear()
        type_of_piece = str(type(self)).split('.')[-1][:-2]
        print('{} located at {} has been locked'.format(type_of_piece, self.location))

    # TODO: [Movement] Implement unlock method; currently have a placeholder for testing
    def unlock(self):
        """
        Called when the piece goes from a position where it cannot move, to a position where it can.
        This function calculates a new list of possible moves for this piece.
        """
        type_of_piece = str(type(self)).split('.')[-1][:-2]
        print('{} located at {} has been unlocked'.format(type_of_piece, self.location))

    @abstractmethod
    def calc_possible_moves(self):
        """
        This is an abstract method that is meant to be implemented in the Piece subclasses. This method calculates
        all possible moves for a given piece based on the current board state.
        """
        pass

    # TODO: [Formatting] Should some of the code in these functions stay in the HexSpace superclass?
    def add_connection_to_piece(self, location):
        HexSpace.add_connection_to_piece(self, location)

    def remove_connection_to_piece(self, location):
        HexSpace.remove_connection_to_piece(self, location)

    def add_connection_to_empty_space(self, location):
        HexSpace.add_connection_to_empty_space(self, location)
        board.HiveGameBoard().empty_spaces[location].add_connection_to_piece(self.location)

    def remove_connection_to_empty_space(self, location):
        HexSpace.remove_connection_to_empty_space(self, location)
