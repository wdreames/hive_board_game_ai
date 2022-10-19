from src.game.spaces import Piece


class Ant(Piece):

    def __init__(self, board_instance, x=0, y=0, is_white=True):
        super().__init__(board_instance, x, y, is_white)
        self.name = Piece.ANT

        if self.is_white:
            self.board.num_white_free_pieces[self.name] += 1
        else:
            self.board.num_black_free_pieces[self.name] += 1

    def remove(self):
        super().remove()
        self.board.ant_locations.remove(self.location)

    def set_location_to(self, new_location):
        super().set_location_to(new_location)
        self.board.ant_locations.add(new_location)

    def calc_possible_moves(self):
        # Can move to any open space that it can slide to
        can_slide_into = self.connected_empty_spaces.difference(self.sliding_prevented_to.keys())
        can_slide_into_prevention_sets = set()
        spaces_in_connected_prevention_sets = set()
        if not can_slide_into:
            self.possible_moves = set()
        else:
            moveset = set(self.board.empty_spaces.keys())
            for prevention_set in self.board.ant_mvt_prevention_sets:
                # If the Ant cannot slide into a given prevention set,
                # those potential moves are removed from the moveset
                overlap_with_prevention_set = can_slide_into.intersection(prevention_set)
                if not overlap_with_prevention_set:
                    moveset = moveset.difference(prevention_set)
                else:
                    can_slide_into_prevention_sets = can_slide_into_prevention_sets.union(overlap_with_prevention_set)
                    spaces_in_connected_prevention_sets = spaces_in_connected_prevention_sets.union(prevention_set)

            # Check if every move the Ant has is within a prevention set. In this scenario, the base set of
            # Empty Spaces are not added into the moveset
            if not can_slide_into.difference(can_slide_into_prevention_sets):
                moveset = spaces_in_connected_prevention_sets

            # Check if any surrounding Empty Spaces are only connected to this Piece. If so, that is not a possible move
            for space_location in can_slide_into.intersection(self.cannot_move_to):
                empty_space = self.board.empty_spaces[space_location]
                if len(empty_space.connected_pieces) == 1 and self.location in empty_space.connected_pieces:
                    moveset.remove(space_location)

            self.possible_moves = moveset
        self.update_board_moves()
        return self.possible_moves


class Beetle(Piece):

    def __init__(self, board_instance, x=0, y=0, is_white=True):
        self.stacked_piece_obj = None

        super().__init__(board_instance, x, y, is_white)
        self.name = Piece.BEETLE

        if self.is_white:
            self.board.num_white_free_pieces[self.name] += 1
        else:
            self.board.num_black_free_pieces[self.name] += 1

    def calc_possible_moves(self):
        # Can move to any space that is possible to move to (including on top of pieces)
        moveset = self.connected_empty_spaces
        if self.stacked_piece_obj is None:
            moveset = moveset.difference(self.cannot_move_to)
        moveset = moveset.union(self.connected_pieces)
        self.possible_moves = moveset
        self.update_board_moves()
        return self.possible_moves

    def lock(self):
        if self.stacked_piece_obj is None:
            super().lock()

    def remove(self):
        on_top_of_piece = self.stacked_piece_obj is not None

        if on_top_of_piece:
            self.stacked_piece_obj.connected_pieces = self.connected_pieces.copy()
            self.stacked_piece_obj.connected_empty_spaces = self.connected_empty_spaces.copy()
            self.stacked_piece_obj.sliding_prevented_to = self.sliding_prevented_to.copy()
            self.stacked_piece_obj.cannot_move_to = self.cannot_move_to.copy()
            self.stacked_piece_obj.preventing_sliding_for = self.preventing_sliding_for.copy()

            # Need to update num white/black connected in nearby empty spaces
            if self.is_white != self.stacked_piece_obj.is_white:
                for connected_emt_spc_loc in self.connected_empty_spaces:
                    connected_emt_spc = self.board.empty_spaces[connected_emt_spc_loc]
                    if self.is_white:
                        connected_emt_spc.num_white_connected -= 1
                        connected_emt_spc.num_black_connected += 1
                    else:
                        connected_emt_spc.num_white_connected += 1
                        connected_emt_spc.num_black_connected -= 1
                    connected_emt_spc.prepare_for_update()

            self.preventing_sliding_for.clear()

            # Remove this piece from the board dictionaries
            self.board.remove_possible_moves(self.location)

            self.board.pieces[self.location] = self.stacked_piece_obj
            self.stacked_piece_obj.prepare_for_update()
            self.stacked_piece_obj.unlock()
            self.stacked_piece_obj = None
        else:
            super().remove()

    def set_location_to(self, new_location):
        moving_onto_piece = new_location in self.board.pieces

        if moving_onto_piece:
            # Move this piece in the board dictionary
            self.location = new_location
            self.x = new_location[0]
            self.y = new_location[1]
            self.stacked_piece_obj = self.board.pieces[new_location]
            self.board.pieces[new_location] = self

            # Copy the connections from the piece at the new lo
            self.connected_pieces = self.stacked_piece_obj.connected_pieces
            self.connected_empty_spaces = self.stacked_piece_obj.connected_empty_spaces
            self.sliding_prevented_to = self.stacked_piece_obj.sliding_prevented_to
            self.cannot_move_to = self.stacked_piece_obj.cannot_move_to
            self.preventing_sliding_for = self.stacked_piece_obj.preventing_sliding_for
            self.linked_grasshoppers = self.stacked_piece_obj.linked_grasshoppers

            # Need to update num white/black connected in nearby empty spaces
            if self.is_white != self.stacked_piece_obj.is_white:
                for connected_emt_spc_loc in self.connected_empty_spaces:
                    connected_emt_spc = self.board.empty_spaces[connected_emt_spc_loc]
                    if self.is_white:
                        connected_emt_spc.num_white_connected += 1
                        connected_emt_spc.num_black_connected -= 1
                    else:
                        connected_emt_spc.num_white_connected -= 1
                        connected_emt_spc.num_black_connected += 1
                    connected_emt_spc.prepare_for_update()

            # Remove piece from board movement dictionaries
            self.stacked_piece_obj.lock()

            self.prepare_for_update()
        else:
            super().set_location_to(new_location)

    def add_connection_to_piece(self, location):
        """
        This method call acts as a proxy for when the Beetle is on top of a Grasshopper. The Grasshopper has specific
        functionality required for pathing. This function call ensures the Grasshopper gathers all the information
        required to retain a correct set of possible moves while it is underneath the Beetle.
        """
        super().add_connection_to_piece(location)
        if self.stacked_piece_obj is not None and self.stacked_piece_obj.name in [Piece.GRASSHOPPER, Piece.BEETLE]:
            self.stacked_piece_obj.add_connection_to_piece(location)

    def remove_grasshopper_path(self, start_location, initial_call=True):
        """
        This method acts as a proxy for when the Beetle is on top of a Grasshopper. The Grasshopper has specific
        functionality required for pathing. This function call ensures the Grasshopper gathers all the information
        required to retain a correct set of possible moves while it is underneath the Beetle.
        """
        if self.stacked_piece_obj is not None and self.stacked_piece_obj.name in [Piece.GRASSHOPPER, Piece.BEETLE]:
            self.stacked_piece_obj.remove_grasshopper_path(start_location, initial_call=initial_call)
        else:
            raise RuntimeError('Beetle is not on top of a Grasshopper but a Grasshopper function call was attempted.')

    def update_spider_path(self, empty_space_location):
        """
        This method acts as a proxy for when the Beetle is on top of a Spider. The Spider has specific
        functionality required for pathing. This function call ensures the Spider gathers all the information
        required to retain a correct set of possible moves while it is underneath the Beetle.
        """
        if self.stacked_piece_obj is not None and self.stacked_piece_obj.name in [Piece.SPIDER, Piece.BEETLE]:
            self.stacked_piece_obj.update_spider_path(empty_space_location)
        else:
            raise RuntimeError('Beetle is not on top of a Spider but a Spider function call was attempted.')

    def remove_spider_path(self, start_location, initial_call=True):
        """
        This method acts as a proxy for when the Beetle is on top of a Spider. The Spider has specific
        functionality required for pathing. This function call ensures the Spider gathers all the information
        required to retain a correct set of possible moves while it is underneath the Beetle.
        """
        if self.stacked_piece_obj is not None and self.stacked_piece_obj.name in [Piece.SPIDER, Piece.BEETLE]:
            self.stacked_piece_obj.remove_spider_path(start_location, initial_call)
        else:
            raise RuntimeError('Beetle is not on top of a Spider but a Spider function call was attempted.')


class Grasshopper(Piece):

    class GrasshopperPath:
        """
        This class is used to store information about Grasshopper movement.
        """

        def __init__(self, location, is_empty_space, previous_location=None, next_location=None, direction=None):
            self.location = location
            self.is_empty_space = is_empty_space
            self.previous_location = previous_location
            self.next_location = next_location
            self.direction = direction

    def __init__(self, board_instance, x=0, y=0, is_white=True):
        self.paths = dict()
        self.paths_to_add = set()
        self.initialize_paths = True

        super().__init__(board_instance, x, y, is_white)
        self.name = Piece.GRASSHOPPER

        if self.is_white:
            self.board.num_white_free_pieces[self.name] += 1
        else:
            self.board.num_black_free_pieces[self.name] += 1

    def update(self):
        # Add any relevant paths
        if self.initialize_paths:
            # Add new paths towards all connected Pieces
            for piece_location in self.connected_pieces:
                self.add_grasshopper_path(piece_location)
            self.initialize_paths = False
        else:
            for path_data in self.paths_to_add:
                self.add_grasshopper_path(path_data.location, path_data.previous_location, path_data.direction)

        self.paths_to_add.clear()

        super().update()

    def calc_possible_moves(self):
        # Moves calculated by adding/removing links with other spaces. This is done separately
        self.update_board_moves()
        return self.possible_moves

    def remove(self):
        # Unlink pieces on the movement path. This needs to happen *before* this grasshopper's location is updated
        for piece_location in self.connected_pieces:
            self.remove_grasshopper_path(piece_location)

        super().remove()
        self.possible_moves.clear()

    def set_location_to(self, new_location):
        super().set_location_to(new_location)
        self.initialize_paths = True
        self.prepare_for_update()

    def add_connection_to_piece(self, location):
        super().add_connection_to_piece(location)
        self.paths_to_add.add(self.GrasshopperPath(location, is_empty_space=False))

    def add_grasshopper_path(self, location, previous_location=None, direction=None):
        """
        Adds a path for the Grasshopper in a specific direction. If the path finds an EmptySpace, that space is added
        as a possible move for the Grasshopper.

        :param location: (x, y)
            Location to add to the path.
        :param previous_location: (x, y)
            Previous location on the path.
            Default is this Grasshoppers location
        :param direction: (delta x, delta y)
            Direction the path is headed.
            Default is the direction from the previous_location to location.
        """
        if previous_location is None:
            previous_location = self.location
        if direction is None:
            direction = self.direction_from_a_to_b(previous_location, location)

        space_is_empty_space = location not in self.board.pieces

        # Determine the next location
        if space_is_empty_space:
            # If the space is an EmptySpace, add a possible move
            if location not in self.get_all_surrounding_locations():
                self.add_move(location)
            self.board.empty_spaces[location].linked_grasshoppers.add(self.location)
            next_location = None
        else:
            self.board.pieces[location].linked_grasshoppers.add(self.location)
            next_location = self.get_next_space_in_direction(location, direction)

        # Log the data
        self.paths[location] = self.GrasshopperPath(
            location=location,
            is_empty_space=space_is_empty_space,
            previous_location=previous_location,
            next_location=next_location,
            direction=direction
        )

        # Continue adding to the path
        if next_location is not None:
            self.add_grasshopper_path(next_location, location, direction)

    def remove_grasshopper_path(self, location, initial_call=True):
        """
        Removes a previously made path from the Grasshopper. If this function finds an EmptySpace, it is removed from
        this Grasshoppers set of possible moves. This function also prepares the Grasshopper to add a new path starting
        the space before the location where the path removal began.

        :param location: (x, y)
            Location to add to the path.
        :param initial_call: bool
            True if this is the first call of this function. False if this is a recursive call.
            Default is True.
        """
        if location not in self.paths:
            return

        # Get the path data at this location
        path_data = self.paths.pop(location)
        if path_data.is_empty_space:
            self.board.empty_spaces[path_data.location].linked_grasshoppers.remove(self.location)
        else:
            self.board.pieces[path_data.location].linked_grasshoppers.remove(self.location)

        # If the location is an EmptySpace, remove the possible move
        if path_data.is_empty_space:
            self.remove_move(path_data.location)

        if initial_call:
            if not path_data.is_empty_space and path_data.location not in self.get_all_surrounding_locations():
                self.add_move(path_data.location)
            if path_data.previous_location != self.location:
                previous_path_data = self.paths[path_data.previous_location]
                self.paths_to_add.add(previous_path_data)
                self.prepare_for_update()

        if path_data.next_location is not None:
            self.remove_grasshopper_path(path_data.next_location, initial_call=False)


class QueenBee(Piece):

    def __init__(self, board_instance, x=0, y=0, is_white=True):
        super().__init__(board_instance, x, y, is_white)
        self.name = Piece.QUEEN_BEE

        if self.is_white:
            self.board.num_white_free_pieces[self.name] += 1
        else:
            self.board.num_black_free_pieces[self.name] += 1

    def update(self):
        super().update()
        self.update_board_location()

    def update_board_location(self):
        """
        Updates the game board to have the current location of this Queen Bee.
        """
        if self.is_white:
            self.board.white_queen_location = self.location
        else:
            self.board.black_queen_location = self.location

    def calc_possible_moves(self):
        # Can move to any open space that it can slide to
        self.possible_moves = self.get_queen_bee_moves()
        self.update_board_moves()
        return self.possible_moves


class Spider(Piece):

    class SpiderPath:
        """
        This class is used to store information about Spider movement.
        """

        def __init__(self, location, path_id, previous_location, next_locations, depth, visited):
            self.location = location
            self.path_id = path_id
            self.previous_location = previous_location
            self.next_locations = next_locations
            self.depth = depth
            self.visited = visited

    def __init__(self, board_instance, x=0, y=0, is_white=True):
        self.previous_path_starts = set()
        self.current_path_id = 0
        self.paths = dict()
        self.path_roots = dict()

        self.paths_to_add = set()
        self.initialize_paths = True

        super().__init__(board_instance, x, y, is_white)
        self.name = Piece.SPIDER

        if self.is_white:
            self.board.num_white_free_pieces[self.name] += 1
        else:
            self.board.num_black_free_pieces[self.name] += 1

    def get_new_path_id(self):
        """
        Each path for the Spider has a unique ID. This function is used to generate a new ID.
        :return: int
            ID for the new path
        """
        self.current_path_id += 1
        return self.current_path_id

    def update(self):
        super().update()

        starts_to_paths = self.get_queen_bee_moves()

        if self.initialize_paths:
            # Add paths in direction of connected empty spaces
            self.paths.clear()
            self.possible_moves.clear()
            for empty_space_location in starts_to_paths:
                self.add_spider_path(empty_space_location)
            self.initialize_paths = False
        else:
            # Add recorded paths to add during update
            for spider_path in self.paths_to_add:
                self.add_spider_path(
                    empty_space_location=spider_path.location,
                    previous_location=spider_path.previous_location,
                    depth=spider_path.depth,
                    path_id=spider_path.path_id,
                    visited=spider_path.visited
                )

            # Compare current path starts to previous path starts
            new_starting_paths = starts_to_paths.difference(self.previous_path_starts)
            removed_starting_paths = self.previous_path_starts.difference(starts_to_paths)

            # If a start path was removed, remove it
            for path_start in removed_starting_paths:
                self.remove_spider_path(path_start)

            # If there is a new start path, add it
            for path_start in new_starting_paths:
                self.add_spider_path(path_start)

        self.paths_to_add.clear()
        self.previous_path_starts = starts_to_paths

    def calc_possible_moves(self):
        # Moves calculated by adding/removing links with other spaces. This is done separately
        self.update_board_moves()
        return self.possible_moves

    def set_location_to(self, new_location):
        super().set_location_to(new_location)
        self.initialize_paths = True
        self.prepare_for_update()

    def remove(self):
        # Get available path starts, remove paths in those directions immediately
        starts_to_paths = self.get_queen_bee_moves()
        for empty_space_location in starts_to_paths:
            self.remove_spider_path(empty_space_location)

        super().remove()

    def update_spider_path(self, empty_space_location):
        """
        Finds any SpiderPaths containing this location. Each path is cleared, and new paths are generated starting at
        the root nodes of each path.

        :param empty_space_location: (x, y)
            Location of the EmptySpace causing an update to a path.
        """
        if empty_space_location in self.paths:
            for path_id, _ in self.paths[empty_space_location].items():
                path_root = self.path_roots[path_id]
                # Need to clear the root of this path and start it fresh.

                self.remove_spider_path(path_root.location, path_id=path_id)
                self.paths_to_add.add(path_root)
                self.prepare_for_update()

    def add_spider_path(self, empty_space_location, previous_location=None, depth=1, path_id=None, visited=None):
        """
        Adds a new path of movement for this Spider. If the depth of the current node in the path is 3, a possible move
        is added to this Spider.

        :param empty_space_location: (x, y)
            Location on the path
        :param previous_location: (x, y)
            Previous location on the path
        :param depth: int
            Depth on the path (number of spaces from the Spider)
        :param path_id: int
            ID of the path
        :param visited: set {(x, y)}
            Set of all visited locations
        """
        # Ensure that this Empty Space is connected to pieces other than this Spider
        empty_space = self.board.empty_spaces.get(empty_space_location)
        if empty_space is None or len(empty_space.connected_pieces) == 1 and self.location in empty_space.connected_pieces:
            return
        if previous_location is None:
            previous_location = self.location
        if path_id is None:
            path_id = self.get_new_path_id()
        if visited is None:
            visited = {previous_location}
        visited.add(empty_space_location)

        # Add a link to the empty space
        empty_space.linked_spiders.add(self.location)

        # Determine which locations to search
        starts_to_paths = self.get_starts_to_paths(empty_space_location, visited)

        # Log the data
        current_path = self.SpiderPath(
            location=empty_space_location,
            path_id=path_id,
            previous_location=previous_location,
            next_locations=starts_to_paths,
            depth=depth,
            visited=visited
        )
        if empty_space_location in self.paths:
            self.paths[empty_space_location][path_id] = current_path
        else:
            self.paths[empty_space_location] = {
                path_id: current_path
            }

        # Add a root node
        if depth == 1:
            self.path_roots[path_id] = current_path

        # Add this Spider's location as a possible move for Spider if depth=2 and Spider in empty_space.connected_pieces
        visited_minus_self = visited.difference({self.location})
        unavailable_moves = self.get_cannot_path_to(empty_space_location).union(visited_minus_self)
        if depth == 2 and self.location in empty_space.connected_pieces.difference(unavailable_moves):
            self.add_move(self.location)
            self.paths[empty_space_location][path_id].next_locations.add(self.location)

        # If depth is 3, add this location as a possible move for the Spider
        if depth >= 3:
            self.add_move(empty_space_location)
            self.paths[empty_space_location][path_id].next_locations.clear()
            return

        # Continue adding empty spaces to the path based on the determinations that were made
        for start_to_path in starts_to_paths.copy():
            self.add_spider_path(start_to_path, empty_space_location, depth + 1, path_id, visited)

    def remove_spider_path(self, empty_space_location, initial_call=True, path_id=None):
        """
        Adds a previously made path of movement for this Spider. If the depth of the current node in the path is 3, a
        possible move is removed from this Spider.

        :param empty_space_location: (x, y)
            Location on the path
        :param initial_call: bool
            True if this is the first call of this function. False if this is a recursive call.
            Default is True.
        :param path_id: int
            ID of the path to be removed. If the ID is None, all paths at this EmptySpace are removed.
            Default is None.
        """
        # Get data stored for this spider location
        if empty_space_location not in self.paths:
            return

        # Get the path data at this location
        location_data = self.paths.pop(empty_space_location)
        self.board.empty_spaces[empty_space_location].linked_spiders.remove(self.location)

        # Check each path stored at this location
        if path_id is not None:
            spider_paths = [location_data[path_id]]
        else:
            spider_paths = [spider_path for spider_path in location_data.values()]

        for spider_path in spider_paths:
            # If depth = 1, remove this from the dictionary of root nodes
            if spider_path.depth == 1:
                self.path_roots.pop(spider_path.path_id)

            # Remove this Spider's location as a possible move for Spider if depth = 2
            # and Spider in empty_space.connected_pieces
            if spider_path.depth == 2 and self.location in spider_path.next_locations:
                self.remove_move(self.location)

            # If depth = 3, remove this location as a possible move for Spider
            if spider_path.depth == 3:
                self.remove_move(spider_path.location)

            if initial_call:
                # Prepare the previous location to add to its path
                previous_location = spider_path.previous_location
                if previous_location != self.location:
                    previous_path_node = self.paths[previous_location][spider_path.path_id]
                    self.paths_to_add.add(previous_path_node)
                    self.prepare_for_update()
                else:
                    self.initialize_paths = True
                    self.prepare_for_update()

            # Call recursive function for next locations
            for next_path_location in spider_path.next_locations:
                self.remove_spider_path(next_path_location, initial_call=False, path_id=spider_path.path_id)

    def get_starts_to_paths(self, empty_space_location, visited):
        """
        Determines directions a SpiderPath can continue moving towards

        :param empty_space_location: (x, y)
            Location of the current node in the SpiderPath
        :param visited: set {(x, y)}
            Set of all previously visited locations along the path
        :return: set {(x, y)}
            Set of all locations this SpiderPath node can path towards
        """
        unavailable_moves = self.get_cannot_path_to(empty_space_location).union(visited)
        empty_space = self.board.empty_spaces[empty_space_location]
        for prevented_location, piece_locations_preventing_mvt in empty_space.sliding_prevented_to.items():
            if self.location not in piece_locations_preventing_mvt:
                unavailable_moves.add(prevented_location)
        return empty_space.connected_empty_spaces.difference(unavailable_moves)

    # TODO: [Organization] Maybe try to find an easier way to do this?
    def get_cannot_path_to(self, location):
        """
        This is a variation on the HexSpace.update_cannot_move_to() function that excludes this Spider from the set of
        Pieces to check.

        This function marks certain locations that the space at the given location cannot move to. In order to move
        somewhere in Hive, you must slide along a Piece. In some cases, there is not a piece to slide against, meaning
        some spaces are unreachable for certain Pieces.

        :param location: (x, y)
            Location of the space to calculate movement rules whilst excluding this Spider's location
        :return: set {(x, y)}
            Set of locations the specified space cannot move to
        """
        x = location[0]
        y = location[1]

        cannot_path_to_set = set()

        cannot_path_to_set.add(self._cannot_path_to_helper((x, y - 1), (x - 1, y - 1), (x + 1, y)))
        cannot_path_to_set.add(self._cannot_path_to_helper((x + 1, y), (x, y - 1), (x + 1, y + 1)))
        cannot_path_to_set.add(self._cannot_path_to_helper((x + 1, y + 1), (x + 1, y), (x, y + 1)))
        cannot_path_to_set.add(self._cannot_path_to_helper((x, y + 1), (x - 1, y), (x + 1, y + 1)))
        cannot_path_to_set.add(self._cannot_path_to_helper((x - 1, y), (x - 1, y - 1), (x, y + 1)))
        cannot_path_to_set.add(self._cannot_path_to_helper((x - 1, y - 1), (x, y - 1), (x - 1, y)))

        return cannot_path_to_set

    def _cannot_path_to_helper(self, location, location_check1, location_check2):
        """
         Helper function. Checks if Pieces exist in the specified locations (location_check1 and
         location_check2).

         :return: (x, y) or None
            Location to add to the set of locations this Spider cannot path to.
         """
        pieces_minus_spider = self.board.pieces.copy()
        pieces_minus_spider.pop(self.location)
        if {location_check1, location_check2}.isdisjoint(pieces_minus_spider):
            return location
        else:
            return None
