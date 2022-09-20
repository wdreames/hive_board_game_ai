import src.game_board.piece as p
import src.game_board.board as board


class Beetle(p.Piece):

    def __init__(self, x=0, y=0, is_white=True):
        super().__init__(x, y, is_white)
        self.name = p.Piece.BEETLE

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
