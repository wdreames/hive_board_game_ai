
class HexSpace:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.location = (self.x, self.y)
        self.connected_pieces = set()
        self.connected_empty_spaces = set()
