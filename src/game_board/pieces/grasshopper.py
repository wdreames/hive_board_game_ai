import src.game_board.piece as p
import src.game_board.board as board


class Grasshopper(p.Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = p.Piece.GRASSHOPPER
        self.spaces_to_link = self.connected_pieces
        self.spaces_to_unlink = set()
        self.prepare_for_update()

    def update(self):
        for space_loc in self.spaces_to_link:
            direction = self.dir_from_a_to_b(self.location, space_loc)
            self.add_gh_links_in_direction(self.location, direction, space_loc)
        for space_loc in self.spaces_to_unlink:
            direction = self.dir_from_a_to_b(self.location, space_loc)
            self.remove_gh_links_in_direction(self.location, direction, space_loc)
        super().update()

    def calc_possible_moves(self):
        # Moves calculated by adding/removing links with other spaces. This is done separately
        self.update_board_moves()
        return self.possible_moves

    def add_connection_to_piece(self, location):
        super().add_connection_to_piece(location)
        self.spaces_to_link.add(location)
        self.prepare_for_update()
        # direction = self.dir_from_a_to_b(self.location, location)
        # self.add_gh_links_in_direction(self.location, direction, start_loc=location)

    def remove(self):
        # Update relevant spaces
        for piece_loc in self.connected_pieces:
            direction = self.dir_from_a_to_b(self.location, piece_loc)
            self.remove_gh_links_in_direction(self.location, direction)
        self.possible_moves.clear()
        super().remove()
