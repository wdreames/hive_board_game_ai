import src.game_board.piece as p
import src.game_board.board as board


class Grasshopper(p.Piece):

    def __init__(self, x=0, y=0, is_white=True):
        self.pieces_to_add_to_path = set()
        self.pieces_to_remove_from_path = set()
        self.added_paths = set()
        self.removed_paths = set()
        super().__init__(x, y, is_white)
        self.name = p.Piece.GRASSHOPPER

    def update(self):
        for piece_location in self.pieces_to_remove_from_path:
            self.remove_path(piece_location)
        for piece_location in self.pieces_to_add_to_path:
            self.add_path(piece_location)

        self.pieces_to_remove_from_path.clear()
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
            self.remove_path(piece_location)

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

    def add_move(self, location):
        self.possible_moves.add(location)

    def remove_move(self, location):
        if location in self.possible_moves:
            self.possible_moves.remove(location)

    def add_path(self, start_location):
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

    def remove_path(self, start_location):
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
