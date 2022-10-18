import src.game.board as board


class HiveGameBoardManager:

    def __new__(cls, new_manager=False):
        if not hasattr(cls, 'instance') or new_manager:
            cls.instance = super(HiveGameBoardManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.root_board = board.HiveGameBoard()
        self.current_board = self.root_board

    def set_current_board(self, new_board):
        self.current_board = new_board

    def get_successor(self, board_instance, action):
        successor_board = board_instance.copy()
        if board_instance != self.root_board:
            del board_instance

        successor_board.perform_action_helper(action)
        self.set_current_board(successor_board)

    def get_board(self):
        return self.root_board

    def get_action_list(self):
        return self.root_board.get_action_list()

    def perform_action(self, action):
        self.root_board.perform_action(action)

    def __str__(self):
        return str(self.current_board)
