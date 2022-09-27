from src.game.spaces import Piece
import src.game.board as board


class Ant(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = Piece.ANT

    # TODO: [Movement] Update this to Ant movement (rather than QB mvt)
    def calc_possible_moves(self):
        # Can move to any open space that it can slide to
        unavailable_moves = self.cannot_move_to.union(self.sliding_prevented_to.keys())
        self.possible_moves = self.connected_empty_spaces.difference(unavailable_moves)
        self.update_board_moves()
        return self.possible_moves


class Beetle(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = Piece.BEETLE

        # Only used when Piece is a Beetle; Needs to be of type Piece; NOT A COORDINATE
        self.stacked_piece_obj = None

    # TODO: [Beetle] Beetle will require a lot of new infrastructure in order to stack on top of pieces
    #       * I could rewrite the remove() and _set_location_to() methods here, but this would be somewhat bad
    #         practice. Although if enough will need to be altered, this could be reasonable.
    #       * OR... I could get a space from HiveGameBoard.get_all_pieces() and gather connections from there. Then I
    #         can implement more specific functionality based on space type.

    def calc_possible_moves(self):
        # Can move to any space that is possible to move to (including on top of pieces)
        self.possible_moves = self.connected_empty_spaces.union(self.connected_pieces).difference(self.cannot_move_to)
        self.update_board_moves()
        return self.possible_moves

    def remove(self):
        on_top_of_piece = self.stacked_piece_obj is not None

        if on_top_of_piece:
            self.stacked_piece_obj.connected_pieces = self.connected_pieces
            self.stacked_piece_obj.connected_empty_spaces = self.connected_empty_spaces
            self.stacked_piece_obj.sliding_prevented_to = self.sliding_prevented_to
            self.stacked_piece_obj.cannot_move_to = self.cannot_move_to
            self.stacked_piece_obj.preventing_sliding_for = self.preventing_sliding_for

            # Need to update num white/black connected in nearby empty spaces
            if self.is_white != self.stacked_piece_obj.is_white:
                for connected_emt_spc_loc in self.connected_empty_spaces:
                    connected_emt_spc = board.HiveGameBoard().empty_spaces[connected_emt_spc_loc]
                    if self.is_white:
                        connected_emt_spc.num_white_connected -= 1
                        connected_emt_spc.num_black_connected += 1
                    else:
                        connected_emt_spc.num_white_connected += 1
                        connected_emt_spc.num_black_connected -= 1
                    connected_emt_spc.prepare_for_update()

            self.preventing_sliding_for.clear()

            # Remove this piece from the board dictionaries
            if self.is_white:
                board.HiveGameBoard().white_possible_moves.pop(self.location)
            else:
                board.HiveGameBoard().black_possible_moves.pop(self.location)

            board.HiveGameBoard().pieces[self.location] = self.stacked_piece_obj
            self.stacked_piece_obj.prepare_for_update()
            self.stacked_piece_obj = None
        else:
            super().remove()

    def _set_location_to(self, new_location):
        moving_onto_piece = new_location in board.HiveGameBoard().pieces

        if moving_onto_piece:
            # Move this piece in the board dictionary
            self.location = new_location
            self.x = new_location[0]
            self.y = new_location[1]
            self.stacked_piece_obj = board.HiveGameBoard().pieces[new_location]
            board.HiveGameBoard().pieces[new_location] = self

            # Copy the connections from the piece at the new lo
            self.connected_pieces = self.stacked_piece_obj.connected_pieces
            self.connected_empty_spaces = self.stacked_piece_obj.connected_empty_spaces
            self.sliding_prevented_to = self.stacked_piece_obj.sliding_prevented_to
            self.cannot_move_to = self.stacked_piece_obj.cannot_move_to
            self.preventing_sliding_for = self.stacked_piece_obj.preventing_sliding_for

            # Need to update num white/black connected in nearby empty spaces
            if self.is_white != self.stacked_piece_obj.is_white:
                for connected_emt_spc_loc in self.connected_empty_spaces:
                    connected_emt_spc = board.HiveGameBoard().empty_spaces[connected_emt_spc_loc]
                    if self.is_white:
                        connected_emt_spc.num_white_connected += 1
                        connected_emt_spc.num_black_connected -= 1
                    else:
                        connected_emt_spc.num_white_connected -= 1
                        connected_emt_spc.num_black_connected += 1
                    connected_emt_spc.prepare_for_update()

            # TODO: [Movement] This could also be done with a lock action
            # Remove piece from board movement dictionaries
            if self.stacked_piece_obj.is_white:
                board.HiveGameBoard().white_possible_moves.pop(self.stacked_piece_obj.location)
            else:
                board.HiveGameBoard().black_possible_moves.pop(self.stacked_piece_obj.location)

            self.prepare_for_update()
        else:
            super()._set_location_to(new_location)


class Grasshopper(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        self.pieces_to_add_to_path = set()
        self.added_paths = set()
        self.removed_paths = set()
        super().__init__(x, y, is_white)
        self.name = Piece.GRASSHOPPER

    def update(self):
        for piece_location in self.pieces_to_add_to_path:
            self.add_grasshopper_path(piece_location)

        self.pieces_to_add_to_path.clear()
        self.added_paths.clear()
        self.removed_paths.clear()

        super().update()

    def calc_possible_moves(self):
        # Moves calculated by adding/removing links with other spaces. This is done separately
        self.update_board_moves()
        return self.possible_moves

    def remove(self):
        # Unlink pieces on the movement path. This needs to happen *before* this grasshopper's location is updated
        for piece_location in self.connected_pieces:
            piece = board.HiveGameBoard().pieces[piece_location]
            piece.remove_from_grasshopper_path(self.location)

        super().remove()
        self.possible_moves.clear()

    def _set_location_to(self, new_location):
        super()._set_location_to(new_location)
        for piece_location in self.connected_pieces:
            board.HiveGameBoard().pieces[piece_location].add_to_grasshopper_path(self.location)

    def add_connection_to_piece(self, location):
        super().add_connection_to_piece(location)
        board.HiveGameBoard().pieces[location].add_to_grasshopper_path(self.location)

    def remove_connection_to_piece(self, location):
        super().remove_connection_to_piece(location)
        board.HiveGameBoard().pieces[location].remove_from_grasshopper_path(self.location)

    def add_grasshopper_path(self, start_location):
        if start_location in self.added_paths:
            return
        if start_location in board.HiveGameBoard().empty_spaces:
            board.HiveGameBoard().empty_spaces[start_location].add_link_to_grasshopper(self.location)
            return

        direction = self.direction_from_a_to_b(self.location, start_location)

        current_location = start_location
        while current_location not in board.HiveGameBoard().empty_spaces:
            if current_location in self.added_paths:
                return
            else:
                board.HiveGameBoard().pieces[current_location].add_link_to_grasshopper(self.location)
                current_location = self.get_next_space_in_direction(current_location, direction)

        # current_location must be an EmptySpace
        board.HiveGameBoard().empty_spaces[current_location].add_link_to_grasshopper(self.location)
        self.add_move(current_location)

    def remove_grasshopper_path(self, start_location):
        if start_location in self.removed_paths:
            return

        direction = self.direction_from_a_to_b(self.location, start_location)

        current_location = start_location
        board.HiveGameBoard().get_all_spaces()[current_location].remove_link_to_grasshopper(self.location)
        if current_location in board.HiveGameBoard().empty_spaces:
            self.remove_move(current_location)
        current_location = self.get_next_space_in_direction(current_location, direction)

        while current_location not in board.HiveGameBoard().empty_spaces:
            if current_location in self.removed_paths:
                return
            else:
                board.HiveGameBoard().pieces[current_location].remove_link_to_grasshopper(self.location)
                current_location = self.get_next_space_in_direction(current_location, direction)

        # current_location must be an EmptySpace
        board.HiveGameBoard().empty_spaces[current_location].remove_link_to_grasshopper(self.location)
        self.remove_move(current_location)


class QueenBee(Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = Piece.QUEEN_BEE

    def update(self):
        super().update()
        self.update_board_location()

    def update_board_location(self):
        if self.is_white:
            board.HiveGameBoard().white_queen_location = self.location
        else:
            board.HiveGameBoard().black_queen_location = self.location

    def calc_possible_moves(self):
        # Can move to any open space that it can slide to
        unavailable_moves = self.cannot_move_to.union(self.sliding_prevented_to.keys())
        self.possible_moves = self.connected_empty_spaces.difference(unavailable_moves)
        self.update_board_moves()
        return self.possible_moves


class Spider(Piece):

    def __init__(self, x=0, y=0, is_white=True):

        """
        Dictionary formatted as the following:
        self.path_data = {
            (EmptySpace1.location): {
                depth = #,
                previous_locations = set(),
                next_locations = set()
            },
            (EmptySpace2.location: {
                ...
            },
            ...
        }
        """
        self.path_data = dict()
        self.previous_path_starts = set()

        # Elements formatted as (empty_space_location, previous_location, starting_depth)
        self.paths_to_add = set()
        self.initialize_paths = True

        super().__init__(x, y, is_white)
        self.name = Piece.SPIDER

    def update(self):
        super().update()

        unavailable_moves = self.cannot_move_to.union(self.sliding_prevented_to.keys())
        starts_to_paths = self.connected_empty_spaces.difference(unavailable_moves)

        if self.initialize_paths:
            # Add paths in direction of connected empty spaces
            self.path_data.clear()
            self.possible_moves.clear()
            for empty_space_location in starts_to_paths:
                # (start_of_path, previous_location, initial_depth)
                self.add_spider_path(empty_space_location, self.location, 1)
            self.initialize_paths = False
        else:
            # Add recorded paths to add during update
            for empty_space_location, previous_location, starting_depth in self.paths_to_add:
                self.add_spider_path(empty_space_location, previous_location, starting_depth)

            # Compare current path starts to previous path starts
            new_starting_paths = starts_to_paths.difference(self.previous_path_starts)
            removed_starting_paths = self.previous_path_starts.difference(starts_to_paths)

            # If a start path was removed, remove it
            for path_start in removed_starting_paths:
                self.remove_spider_path(path_start, initial_call=True)

            # If there is a new start path, add it
            for path_start in new_starting_paths:
                self.add_spider_path(path_start, self.location, depth=1)

        self.paths_to_add.clear()
        self.previous_path_starts = starts_to_paths

    def calc_possible_moves(self):
        # Moves calculated by adding/removing links with other spaces. This is done separately
        self.update_board_moves()
        return self.possible_moves

    def _set_location_to(self, new_location):
        super()._set_location_to(new_location)
        self.initialize_paths = True
        self.prepare_for_update()

    def remove(self):
        # Get available path starts, remove paths in those directions immediately
        unavailable_moves = self.cannot_move_to.union(self.sliding_prevented_to.keys())
        starts_to_paths = self.connected_empty_spaces.difference(unavailable_moves)
        for empty_space_location in starts_to_paths:
            self.remove_spider_path(empty_space_location, initial_call=True)

        super().remove()

    def add_spider_path(self, empty_space_location, previous_location, depth):
        # Ensure that this Empty Space is connected to pieces other than this Spider
        empty_space = board.HiveGameBoard().empty_spaces.get(empty_space_location)
        if empty_space is None or len(empty_space.connected_pieces) == 1 and self.location in empty_space.connected_pieces:
            if previous_location != self.location and previous_location in self.path_data:
                if empty_space_location in self.path_data[previous_location]['next_locations']:
                    self.path_data[previous_location]['next_locations'].remove(empty_space_location)
            return

        # Add a link to the empty space
        empty_space.linked_spiders.add(self.location)

        # Determine which locations to search:
        unavailable_moves = empty_space.cannot_move_to.union(empty_space.sliding_prevented_to.keys())
        unavailable_moves.add(previous_location)
        starts_to_paths = empty_space.connected_empty_spaces.difference(unavailable_moves)

        # Add this Spider's location as a possible move for Spider if depth=2 and Spider in empty_space.connected_pieces
        if depth == 2 and self.location in starts_to_paths:
            self.add_move(self.location)

        # Log the data
        if empty_space_location not in self.path_data:
            self.path_data[empty_space_location] = {
                'depth': depth,
                'previous_locations': {previous_location},
                'next_locations': starts_to_paths
            }
        else:
            # TODO: [Spider] Determine if the commented out stmt is necessary
            # if self.path_data[empty_space_location]['depth'] < depth:
            #     return
            self.path_data[empty_space_location]['depth'] = depth
            self.path_data[empty_space_location]['previous_locations'].add(previous_location)
            self.path_data[empty_space_location]['next_locations'] = starts_to_paths

        # If depth is 3, add this location as a possible move for the Spider
        if depth >= 3:
            self.add_move(empty_space_location)
            self.path_data[empty_space_location]['next_locations'].clear()
            return

        # Continue adding empty spaces to the path based on the determinations that were made
        for start_to_path in starts_to_paths.copy():
            self.add_spider_path(start_to_path, empty_space_location, depth + 1)

    def remove_spider_path(self, empty_space_location, initial_call=False):
        # Get data stored for this spider location
        if empty_space_location in self.path_data:
            location_data = self.path_data[empty_space_location]
        else:
            return

        # If depth = 3, remove this location as a possible move for Spider
        if location_data['depth'] == 3:
            self.remove_move(empty_space_location)

        # Remove this Spider's location as a possible move for Spider if depth = 2
        # and Spider in empty_space.connected_pieces
        if location_data['depth'] == 2 and self.location in location_data['next_locations']:
            self.remove_move(self.location)

        if initial_call:
            for previous_location in location_data['previous_locations']:
                if previous_location in self.path_data:
                    if empty_space_location in self.path_data[previous_location]['next_locations']:
                        self.path_data[previous_location]['next_locations'].remove(empty_space_location)
                    for previous_previous_location in self.path_data[previous_location]['previous_locations']:
                        previous_location_depth = self.path_data[previous_location]['depth']
                        path_to_add = (previous_location, previous_previous_location, previous_location_depth)
                        self.paths_to_add.add(path_to_add)
                    self.prepare_for_update()

        # Call recursive function for next locations
        for next_location in location_data['next_locations']:
            self.remove_spider_path(next_location)

        # Clear data stored for this spider location
        self.path_data.pop(empty_space_location)
        board.HiveGameBoard().empty_spaces[empty_space_location].linked_spiders.remove(self.location)

