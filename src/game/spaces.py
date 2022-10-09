import src.game.board as board
from abc import abstractmethod


class HexSpace:
    """
    This is a single space on the Hive game board. This is the superclass for Pieces and Empty Spaces
    """

    def __init__(self, x=0, y=0):
        """
        Initialize values for a space on the board

        :param x: int
            x location
        :param y: int
            y location
        """
        self.x = x
        self.y = y
        self.location = (self.x, self.y)
        self.connected_pieces = set()
        self.connected_empty_spaces = set()
        self.cannot_move_to = set()
        self.sliding_prevented_to = dict()

        self.linked_grasshoppers = set()

    def prepare_for_update(self):
        """
        Notifies the game board that this HexSpace should be updated at the end of the current turn.
        """
        board.HiveGameBoard().spaces_requiring_updates.add(self.location)

    # TODO: Documentation
    def update(self):
        """
        Updates information stored for this HexSpace.
        This involves:
        - Updating self.cannot_move_to
        """
        self.update_cannot_move_to()

    def update_cannot_move_to(self):
        """
        This function marks certain locations that this space cannot move to. In order to move somewhere in Hive, you
        must slide along a Piece. In some cases, there is not a piece to slide against, meaning some spaces are
        unreachable for certain Pieces.
        """
        x = self.x
        y = self.y

        self._add_to_cannot_move_to((x, y - 1), (x - 1, y - 1), (x + 1, y))
        self._add_to_cannot_move_to((x + 1, y), (x, y - 1), (x + 1, y + 1))
        self._add_to_cannot_move_to((x + 1, y + 1), (x + 1, y), (x, y + 1))
        self._add_to_cannot_move_to((x, y + 1), (x - 1, y), (x + 1, y + 1))
        self._add_to_cannot_move_to((x - 1, y), (x - 1, y - 1), (x, y + 1))
        self._add_to_cannot_move_to((x - 1, y - 1), (x, y - 1), (x - 1, y))

    def _add_to_cannot_move_to(self, move_location, piece_location_check1, piece_location_check2):
        """
        Helper function. Checks if Pieces exist in the specified locations (piece_location_check1 and
        piece_location_check2). If not, move_location is marked as a spot this HexSpace cannot move to.
        """
        pieces = board.HiveGameBoard().pieces
        if {piece_location_check1, piece_location_check2}.isdisjoint(pieces):
            self.cannot_move_to.add(move_location)
        elif move_location in self.cannot_move_to:
            self.cannot_move_to.remove(move_location)

    def add_sliding_prevention(self, prevented_space_location, piece_blocking_mvt_location):
        """
        Based on the rules of Hive, Ants, Queen Bees, and Spiders must all slide on the game board rather than be
        picked up. Because of this, there can be certain locations these pieces cannot move into even if the space is
        open.

        This method is used to mark a location as unavailable, and allows the HexSpace to know that it cannot move
        into that space.

        :param prevented_space_location:
            Coordinate (x, y) that has beem blocked
        :param piece_blocking_mvt_location:
            Coordinate (x, y) of the Piece that is blocking movement.
        """
        if prevented_space_location in self.sliding_prevented_to:
            self.sliding_prevented_to[prevented_space_location].add(piece_blocking_mvt_location)
        else:
            self.sliding_prevented_to[prevented_space_location] = {piece_blocking_mvt_location}
        self.prepare_for_update()

    def remove_sliding_prevention(self, prevented_space_location, piece_blocking_mvt_location):
        """
        Based on the rules of Hive, Ants, Queen Bees, and Spiders must all slide on the game board rather than be
        picked up. Because of this, there can be certain locations these pieces cannot move into even if the space is
        open.

        This method is used to mark a location as available again, and allows the HexSpace to know that it is no longer
        prevented from moving into that space.

        :param prevented_space_location:
            Coordinate (x, y) that is no longer blocked
        :param piece_blocking_mvt_location:
            Coordinate (x, y) of the Piece that is no longer blocking movement.
        """

        # The limited space is no longer blocked by this piece
        self.sliding_prevented_to[prevented_space_location].remove(piece_blocking_mvt_location)

        # There are always two pieces preventing sliding. The other piece no longer has a pair and can
        # be cleared as well
        other_limiting_piece_location = self.sliding_prevented_to[prevented_space_location].pop()
        other_limiting_piece_obj = board.HiveGameBoard().get_all_spaces()[other_limiting_piece_location]
        other_limiting_piece_obj.preventing_sliding_for[self.location].remove(prevented_space_location)

        # The limited space is able to slide into the specified location now
        self.sliding_prevented_to.pop(prevented_space_location)

        self.prepare_for_update()

    @staticmethod
    def direction_from_a_to_b(piece_a, piece_b):
        """
        Returns the direction from location a to location b. The values returned will always be within the set returned
        by self.get_all_surrounding_locations().
        Example: is location a is at (0, 1) and location b is at (3, 4), then the direction will be (1, 1).

        :param piece_a:
            coordinate (x, y)
        :param piece_b:
            coordinate (x, y)
        :return:
            direction coordinate (delta x, delta y)
        """
        x_diff = piece_b[0] - piece_a[0]
        y_diff = piece_b[1] - piece_a[1]
        divisor = max(abs(x_diff), abs(y_diff))
        if divisor == 0:
            return 0, 0
        else:
            return x_diff // divisor, y_diff // divisor

    @staticmethod
    def get_next_space_in_direction(start_location, direction):
        """
        Returns the next space on the game board based on a starting location and a direction.
        Example: If the location is (2, 3) and the direction is (1, 0), then the returned location will be (3, 3).

        :param start_location:
            coordinate (x, y)
        :param direction:
            coordinate (delta x, delta y)
        :raises ValueError:
            A ValueError will be raised if a direction of (0, 0) is inputted.
        :return:
            Returns the next space in the given direction.
            If the location is not in the game board, then None is returned instead.
        """
        # If the direction is 0, this would return the same location, possibly leading to an infinite loop
        if direction == (0, 0):
            raise ValueError('Direction cannot be (0, 0).')

        new_location = (start_location[0] + direction[0], start_location[1] + direction[1])
        if new_location in board.HiveGameBoard().get_all_spaces():
            return new_location
        else:
            return None

    def get_all_surrounding_locations(self):
        """
        Returns all locations surrounding this HexSpace

        :return: set of locations
        """
        return {(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x + 1, self.y),
                (self.x + 1, self.y + 1), (self.x, self.y + 1), (self.x - 1, self.y)}

    def get_queen_bee_moves(self):
        """
        Returns the set of moves that would be available if this HexSpace was a Queen Bee.

        :return: set of locations
        """

        unavailable_moves = self.cannot_move_to.union(self.sliding_prevented_to.keys())
        queen_bee_moves = self.connected_empty_spaces.difference(unavailable_moves)
        return queen_bee_moves

    def get_total_num_connections(self):
        """
        Returns the total number of connections for this HexSpace. That is, the number of connected Pieces
        combined with the number of connected EmptySpaces.

        :return: integer representing the total number of connections for this HexSpace
        """
        return len(self.connected_pieces) + len(self.connected_empty_spaces)

    @abstractmethod
    def remove(self):
        """
        Removes this HexSpace from the game board.
        """
        pass

    def add_connection_to_piece(self, location):
        """
        Connects this HexSpace to a Piece at the specified location.

        :param location:
            Coordinate (x, y) of the Piece.
        """
        self.connected_pieces.add(location)
        self.prepare_for_update()

    def remove_connection_to_piece(self, location):
        """
        This HexSpace removes a connection previously made to a Piece at the specified location.

        :param location:
            Coordinate (x, y) of the Piece.
        """
        self.connected_pieces.remove(location)
        self.prepare_for_update()

    def add_connection_to_empty_space(self, location):
        """
        Connects this HexSpace to an EmptySpace at the specified location.

        :param location:
            Coordinate (x, y) of the EmptySpace.
        """
        self.connected_empty_spaces.add(location)
        self.prepare_for_update()

    def remove_connection_to_empty_space(self, location):
        """
        This HexSpace removes a connection previously made to a EmptySpace at the specified location.

        :param location:
            Coordinate (x, y) of the EmptySpace.
        """
        self.connected_empty_spaces.remove(location)
        self.prepare_for_update()


class EmptySpace(HexSpace):
    """
    Used to represent an empty space containing no pieces on the board. These are used when calculating
    where pieces can be placed or moved.
    """

    # TODO: Update Documentation
    def __init__(self, x=0, y=0, connected_pcs=None, connected_emt_spcs=None, sliding_prevented_to=None,
                 cannot_move_to=None):
        """
        Create a new Empty Space at (x, y). This method also allows the Empty Space to connect to any other surrounding
        spaces on the board.

        :param x: int
            x location
        :param y: int
            y location
        :param connected_pcs: set
            Connected pieces to assign to this empty space. If this is None, connected pieces will be calculated
        :param connected_emt_spcs: set
                Connected empty pieces to assign to this empty space. If this is None, connected empty spaces will be
                calculated.
        """
        super().__init__(x, y)
        self.pieces_that_can_move_here = set()
        self.num_white_connected = 0
        self.num_black_connected = 0

        self.linked_spiders = set()
        self.previous_queen_bee_moves = set()

        board.HiveGameBoard().empty_spaces[self.location] = self

        # TODO: [Efficiency] This may not need to be called *every* time an Empty Space is placed
        for ant_location in board.HiveGameBoard().ant_locations:
            board.HiveGameBoard().pieces[ant_location].prepare_for_update()

        # TODO: [Formatting] Clean this up

        if connected_pcs is None or connected_emt_spcs is None:
            # Check surrounding spaces and connect to them
            for space_location in self.get_all_surrounding_locations():
                all_spaces = board.HiveGameBoard().get_all_spaces()
                if space_location in all_spaces:
                    all_spaces[space_location].add_connection_to_empty_space(self.location)
        else:
            # Update connections
            # Assumes the other pieces/empty_spaces will be connected to this empty space on their own
            self.connected_pieces = connected_pcs
            self.connected_empty_spaces = connected_emt_spcs
            self.sliding_prevented_to = sliding_prevented_to
            self.cannot_move_to = cannot_move_to

            surrounding_moves = self.get_queen_bee_moves()
            found_free_space = False
            prevention_set_index = -1

            # Check for connected spaces in prevention sets
            for space_location in surrounding_moves:
                # TODO: [Efficiency] The methods I'm using don't feel super efficient. Looks like O(n^2) here
                current_index = board.HiveGameBoard().empty_space_in_ant_movement_prevention_set(space_location)

                # Found a connected prevention set
                if current_index > -1:
                    # If a prevention set has already been found, union them
                    if prevention_set_index > -1:
                        prevention_set_index = board.HiveGameBoard().union_ant_movement_prevention_sets(current_index,
                                                                                                        prevention_set_index)
                    # Otherwise, store the current index
                    else:
                        prevention_set_index = current_index
                # Found a free space
                else:
                    found_free_space = True

            # If 1+ connected free spaces, clear connected prevention sets
            if found_free_space and prevention_set_index > -1:
                board.HiveGameBoard().clear_ant_movement_prevention_set(prevention_set_index)
            # If only 1 connected prevention set, join it
            elif prevention_set_index > -1:
                board.HiveGameBoard().ant_mvt_prevention_sets[prevention_set_index].add(self.location)
            elif not found_free_space:
                raise RuntimeError('Error! This line should never be called!')

            self.prepare_for_update()

    # TODO: Documentation
    def update(self):
        if len(self.connected_pieces) == 0:
            self.remove()
            return

        super().update()
        self.update_placement_options()

        # Check if a Spider path needs to be updated
        queen_bee_moves = self.get_queen_bee_moves()
        if self.previous_queen_bee_moves != queen_bee_moves:
            self.previous_queen_bee_moves = queen_bee_moves
            for spider_location in self.linked_spiders.copy():
                if spider_location in board.HiveGameBoard().pieces:
                    board.HiveGameBoard().pieces[spider_location].update_spider_path(self.location)
                else:
                    self.linked_spiders.remove(spider_location)

    def update_placement_options(self):
        """
        Determines if white or black pieces can be placed here based on the number of connected pieces.
        If only white pieces have been connected, a white piece can be placed here.
        If only black pieces have been connected, a black piece can be placed here.
        Otherwise, no pieces can be placed here.
        """
        if self.white_can_place():
            board.HiveGameBoard().white_locations_to_place.add(self.location)
            if self.location in board.HiveGameBoard().black_locations_to_place:
                board.HiveGameBoard().black_locations_to_place.remove(self.location)
        elif self.black_can_place():
            board.HiveGameBoard().black_locations_to_place.add(self.location)
            if self.location in board.HiveGameBoard().white_locations_to_place:
                board.HiveGameBoard().white_locations_to_place.remove(self.location)
        else:
            if self.location in board.HiveGameBoard().black_locations_to_place:
                board.HiveGameBoard().black_locations_to_place.remove(self.location)
            if self.location in board.HiveGameBoard().white_locations_to_place:
                board.HiveGameBoard().white_locations_to_place.remove(self.location)

    # TODO: Update Documentation
    def remove(self):
        """
        Removes this empty space from the game board. This also removes this spot from each player's list of locations
        to place pieces, and disconnects any previously connected spaces.
        """
        if self.location in board.HiveGameBoard().white_locations_to_place:
            board.HiveGameBoard().white_locations_to_place.remove(self.location)
        if self.location in board.HiveGameBoard().black_locations_to_place:
            board.HiveGameBoard().black_locations_to_place.remove(self.location)

        for space_location in self.connected_pieces.union(self.connected_empty_spaces):
            board.HiveGameBoard().get_all_spaces()[space_location].remove_connection_to_empty_space(self.location)

        # If this Empty Space is part of a path for a spider, remove the path.
        for spider_location in self.linked_spiders.copy():
            if spider_location in board.HiveGameBoard().pieces:
                spider = board.HiveGameBoard().pieces[spider_location]
                spider.remove_spider_path(self.location)

        # If this Empty Space is part of a path for a grasshopper, remove the path.
        for grasshopper_location in self.linked_grasshoppers.copy():
            if grasshopper_location in board.HiveGameBoard().pieces:
                grasshopper = board.HiveGameBoard().pieces[grasshopper_location]
                grasshopper.remove_grasshopper_path(self.location)

        # TODO: [Efficiency] This may not need to be called *every* time an Empty Space is placed
        for ant_location in board.HiveGameBoard().ant_locations:
            board.HiveGameBoard().pieces[ant_location].prepare_for_update()

        board.HiveGameBoard().empty_spaces.pop(self.location)

        del self

    def white_can_place(self):
        """
        Checks if white can place a piece on this empty space

        :return: bool
            True if white can place a piece here; False otherwise
        """
        return not self.num_black_connected

    def black_can_place(self):
        """
        Checks if black can place a piece on this empty space

        :return: bool
            True if black can place a piece here; False otherwise
        """
        return not self.num_white_connected

    # TODO: Documentation
    def add_connection_to_piece(self, location):
        super().add_connection_to_piece(location)
        if board.HiveGameBoard().pieces[location].is_white:
            self.num_white_connected += 1
        else:
            self.num_black_connected += 1

    # TODO: Documentation
    def remove_connection_to_piece(self, location):
        super().remove_connection_to_piece(location)

        if board.HiveGameBoard().pieces[location].is_white:
            self.num_white_connected -= 1
        else:
            self.num_black_connected -= 1

        self.prepare_for_update()

    # TODO: Documentation
    def add_connection_to_empty_space(self, location):
        super().add_connection_to_empty_space(location)
        board.HiveGameBoard().empty_spaces[location].connected_empty_spaces.add(self.location)

    # TODO: Documentation
    def remove_connection_to_empty_space(self, location):
        super().remove_connection_to_empty_space(location)

    def __str__(self):
        return_str = 'Information for EmptySpace at {}:\n'.format(self.location)
        return_str += 'connected_pieces: {}\n'.format(self.connected_pieces)
        return_str += 'connected_empty_spaces: {}\n'.format(self.connected_empty_spaces)
        return_str += 'cannot_move_to: {}\n'.format(self.cannot_move_to)
        return_str += 'sliding_prevented_to: {}\n'.format(self.sliding_prevented_to)
        return_str += f'pieces_that_can_move_here: {self.pieces_that_can_move_here}\n'
        return_str += f'num_white_connected: {self.num_white_connected}\n'
        return_str += f'num_black_connected: {self.num_black_connected}\n'
        return_str += f'linked_spiders: {self.linked_spiders}\n'

        return return_str


class Piece(HexSpace):
    """
    Used to represent a piece on the game board. This is an abstract class.
    Superclass for Ant, Beetle, Grasshopper, QueenBee, and Spider.
    """

    GENERIC = 'Generic Piece'
    ANT = 'Ant'
    BEETLE = 'Beetle'
    GRASSHOPPER = 'Grasshopper'
    QUEEN_BEE = 'Queen Bee'
    SPIDER = 'Spider'

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
        self.name = Piece.GENERIC
        self.is_white = is_white
        self.possible_moves = set()
        self.can_move = True
        self.preventing_sliding_for = {}

        # TODO: [Organization] This assumes that this color piece can be placed here without issue
        if self.location in board.HiveGameBoard().empty_spaces:
            self.set_location_to(self.location)
        else:
            raise RuntimeError('No empty space at {} to place a new {}'.format(self.location, self.name))

    # TODO: Documentation
    def update(self):
        super().update()
        self.calc_possible_moves()

    # TODO: Documentation
    def move_to(self, new_location):
        self.remove()
        self.set_location_to(new_location)

    # TODO: Documentation
    def remove(self):
        # Update pieces that are no longer prevented from sliding
        all_spaces = board.HiveGameBoard().get_all_spaces()
        for limited_space_loc, locations in self.preventing_sliding_for.items():
            limited_space = all_spaces[limited_space_loc]

            for loc in locations:
                # The limited space is no longer blocked by this piece
                limited_space.remove_sliding_prevention(loc, self.location)

                # limited_space_loc and loc are a piar of spaces prevented from sliding
                if limited_space_loc in board.HiveGameBoard().empty_spaces and \
                        loc in board.HiveGameBoard().empty_spaces:
                    space1_prevention_index = board.HiveGameBoard().empty_space_in_ant_movement_prevention_set(
                        limited_space_loc)
                    space2_prevention_index = board.HiveGameBoard().empty_space_in_ant_movement_prevention_set(loc)

                    # Both are empty spaces in different ant movement prevention sets
                    if space1_prevention_index > -1 and space2_prevention_index > -1:
                        if space1_prevention_index != space2_prevention_index:
                            board.HiveGameBoard().union_ant_movement_prevention_sets(space1_prevention_index,
                                                                                     space2_prevention_index)
                    # Only one is an empty space
                    elif space1_prevention_index > -1:
                        board.HiveGameBoard().clear_ant_movement_prevention_set(space1_prevention_index)
                    elif space2_prevention_index > -1:
                        board.HiveGameBoard().clear_ant_movement_prevention_set(space2_prevention_index)

        # Create a new empty space here
        EmptySpace(self.x, self.y, self.connected_pieces, self.connected_empty_spaces, self.sliding_prevented_to,
                   self.cannot_move_to)

        self.update_one_hive_rule(self_is_placing=False)

        all_board_spaces = board.HiveGameBoard().get_all_spaces()
        for space in self.connected_pieces.union(self.connected_empty_spaces):
            all_board_spaces[space].remove_connection_to_piece(self.location)
            all_board_spaces[space].add_connection_to_empty_space(self.location)

        # If this Piece is part of a path for a grasshopper, remove the path.
        for grasshopper_location in self.linked_grasshoppers.copy():
            if grasshopper_location in board.HiveGameBoard().pieces:
                grasshopper = board.HiveGameBoard().pieces[grasshopper_location]
                grasshopper.remove_grasshopper_path(self.location)

        self.linked_grasshoppers.clear()

        self.preventing_sliding_for.clear()

        # Remove this piece from the board dictionaries
        board.HiveGameBoard().remove_possible_moves(self.location)

        board.HiveGameBoard().pieces.pop(self.location)

    # TODO: Documentation
    # TODO: [Formatting] Reformat this function for added readability
    def set_location_to(self, new_location):
        """
        Moves this piece to a new location. This also updates any previous/new connections to other pieces. No movement
        will happen if the move is invalid.

        :param new_location: tuple
            (x, y) location where the piece will be placed
        """
        # Move this piece in the board dictionary
        self.location = new_location
        self.x = new_location[0]
        self.y = new_location[1]
        board.HiveGameBoard().pieces[new_location] = self

        # Copy the connections from the empty space at the new location
        related_empty_space = board.HiveGameBoard().empty_spaces[new_location]
        self.connected_pieces = related_empty_space.connected_pieces
        self.connected_empty_spaces = related_empty_space.connected_empty_spaces
        self.sliding_prevented_to = related_empty_space.sliding_prevented_to
        self.cannot_move_to = related_empty_space.cannot_move_to

        # Update all the piece and empty space connections
        all_connected_spaces = self.connected_empty_spaces.union(self.connected_pieces)
        for space_location in all_connected_spaces:
            board.HiveGameBoard().get_all_spaces()[space_location].add_connection_to_piece(self.location)

        # Delete the empty space at this location
        related_empty_space.remove()

        self._create_surrounding_emt_spcs()

        self._update_sliding()

        self.update_one_hive_rule(self_is_placing=True)

    # TODO: Documentation
    def _create_surrounding_emt_spcs(self):
        # Helper function for move_to(location)
        # Add new empty spaces
        all_connected_spaces = self.connected_empty_spaces.union(self.connected_pieces)
        surrounding_locations = {(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x - 1, self.y),
                                 (self.x + 1, self.y),
                                 (self.x, self.y + 1), (self.x + 1, self.y + 1)}
        locations_for_new_empty_spaces = surrounding_locations.difference(all_connected_spaces)

        for point in locations_for_new_empty_spaces:
            EmptySpace(point[0], point[1])

    # TODO: Documentation
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

    # TODO: Documentation
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

            space1.add_sliding_prevention(space2_loc, self.location)
            space1.add_sliding_prevention(space2_loc, other_piece_loc)
            space2.add_sliding_prevention(space1_loc, self.location)
            space2.add_sliding_prevention(space1_loc, other_piece_loc)

            # Update Ant movement prevention sets
            if space1_loc in board.HiveGameBoard().empty_spaces and space2_loc in board.HiveGameBoard().empty_spaces:
                space1_prevention_index = board.HiveGameBoard().empty_space_in_ant_movement_prevention_set(space1_loc)
                space2_prevention_index = board.HiveGameBoard().empty_space_in_ant_movement_prevention_set(space2_loc)

                # Both empty spaces are free spaces
                if space1_prevention_index == -1 and space2_prevention_index == -1:
                    # Determine which space (if any) if on the outside of the board
                    space1_on_outside = space1.get_total_num_connections() < 6
                    space2_on_outside = space2.get_total_num_connections() < 6

                    if not space1_on_outside and not space2_on_outside:
                        board.HiveGameBoard().ant_mvt_preventions_to_add.add(space1_loc)
                        board.HiveGameBoard().ant_mvt_preventions_to_add.add(space2_loc)
                    elif space1_on_outside:
                        board.HiveGameBoard().ant_mvt_preventions_to_add.add(space2_loc)
                    elif space2_on_outside:
                        board.HiveGameBoard().ant_mvt_preventions_to_add.add(space1_loc)
                    else:
                        raise RuntimeError('Error! This line should never be executed!')
                else:
                    raise RuntimeError('Error! This line should never be executed!')

    # TODO: Documentation
    # TODO: [Formatting] Put this function into a utils class
    @staticmethod
    def _helper_add_to_dict_set(dictionary, key, value):
        if key in dictionary:
            dictionary[key].add(value)
        else:
            dictionary[key] = {value}

    # TODO: Documentation
    def update_one_hive_rule(self, self_is_placing=True):
        n = len(self.connected_pieces)

        if n == 1:
            if self_is_placing:
                board.HiveGameBoard().pieces[list(self.connected_pieces)[0]].lock()
            else:
                board.HiveGameBoard().pieces[list(self.connected_pieces)[0]].unlock()
            return
        elif n == 6:
            return
        else:
            board.HiveGameBoard().prepare_to_find_articulation_pts = True
            return

    # TODO: Documentation
    def lock(self):
        self.can_move = False
        self.calc_possible_moves()

    # TODO: Documentation
    def unlock(self):
        self.can_move = True
        self.calc_possible_moves()

    @abstractmethod
    def calc_possible_moves(self):
        """
        This is an abstract method that is meant to be implemented in the Piece subclasses. This method calculates
        all possible moves for a given piece based on the current board state.
        """
        pass

    # TODO: Documentation
    def add_move(self, location):
        self.possible_moves.add(location)

    # TODO: Documentation
    def remove_move(self, location):
        if location in self.possible_moves:
            self.possible_moves.remove(location)

    # TODO: Documentation
    def update_board_moves(self):
        if self.can_move:
            board.HiveGameBoard().add_possible_moves(self.location)
        else:
            board.HiveGameBoard().remove_possible_moves(self.location)

    # TODO: Documentation
    def add_connection_to_piece(self, location):
        super().add_connection_to_piece(location)

    # TODO: Documentation
    def remove_connection_to_piece(self, location):
        super().remove_connection_to_piece(location)

    # TODO: Documentation
    def add_connection_to_empty_space(self, location):
        super().add_connection_to_empty_space(location)
        board.HiveGameBoard().empty_spaces[location].add_connection_to_piece(self.location)

    # TODO: Documentation
    def remove_connection_to_empty_space(self, location):
        super().remove_connection_to_empty_space(location)

    def __str__(self):
        return_str = 'Piece information for {} at {}:\n'.format(self.name, self.location)
        return_str += 'Player: {}\n'.format('White' if self.is_white else 'Black')
        return_str += 'connected_pieces: {}\n'.format(self.connected_pieces)
        return_str += 'connected_empty_spaces: {}\n'.format(self.connected_empty_spaces)
        return_str += 'possible_moves: {}\n'.format(self.possible_moves)
        return_str += 'cannot_move_to: {}\n'.format(self.cannot_move_to)
        return_str += 'sliding_prevented_to: {}\n'.format(self.sliding_prevented_to)
        return_str += 'preventing_sliding_for: {}\n'.format(self.preventing_sliding_for)

        return return_str
