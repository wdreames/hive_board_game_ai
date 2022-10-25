from abc import abstractmethod, ABC
import src.game.board as board
import random


class Agent:

    def __init__(self, is_white=True, board_manager=None):
        if board_manager is None:
            board_manager = board.BoardManager()

        self.is_white = is_white
        self.board_manager = board_manager
        self.actions_performed = []

        self.name = 'Agent'

    def get_action(self):
        chosen_action = self.get_action_selection()
        self.actions_performed.append(chosen_action)
        return chosen_action

    @abstractmethod
    def get_action_selection(self):
        pass

    def __str__(self):
        return self.name


class Player(Agent):

    def __init__(self, is_white=True, board_manager=None):
        super().__init__(is_white, board_manager)
        self.name = 'Player'

    def get_action_selection(self):
        actions = self.board_manager.get_action_list()

        print(f'The following actions can be played:')
        for i, action in enumerate(actions):
            print(f'{i + 1}: {action}')

        selection = input('Select an action:')
        if not selection.isnumeric() or int(selection) not in range(1, len(actions) + 1):
            print('Invalid selection. You must enter an integer value from the list of available actions.')
            return self.get_action_selection()

        selected_action = actions[int(selection) - 1]
        return selected_action


class RandomActionAI(Agent):

    def __init__(self, is_white=True, board_manager=None):
        super().__init__(is_white, board_manager)
        self.name = 'Random Action AI'

    def get_action_selection(self):
        actions = self.board_manager.get_action_list()
        rand_index = random.randint(0, len(actions) - 1)
        return actions[rand_index]


class BestNextMoveAI(Agent):

    def __init__(self, is_white=True, board_manager=None, winning_value=50000):
        super().__init__(is_white, board_manager)
        self.name = 'Best Next Move AI'
        self.winning_value = winning_value

    def get_action_selection(self):
        actions = self.board_manager.get_action_list()

        # For every action, get the board's successive state and its evaluation
        # Choose a random action out of those with the highest evaluation

        best_evaluation = -float("inf")
        best_actions = []
        for i, action in enumerate(actions):
            evaluation = self.board_manager.get_successor(action=action).evaluate_state()
            if not self.is_white:
                evaluation *= -1
            # print(f'{self} - Processing action: {str(action):40} Evaluation: {evaluation:2}; {(i+1)/(len(actions)+1)*100:.1f}% complete.')

            if evaluation >= self.winning_value:
                return action
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_actions.clear()
            if evaluation >= best_evaluation:
                best_actions.append(action)

        rand_index = random.randint(0, len(best_actions) - 1)
        return best_actions[rand_index]

    def __str__(self):
        return 'Best Next Move AI'


class MinimaxAI(Agent):

    def __init__(self, is_white=True, board_manager=None, max_depth=4, winning_value=50000):
        super().__init__(is_white, board_manager)
        self.max_depth = max_depth
        self.name = f'Minimax AI with Depth {self.max_depth}'
        self.winning_value = winning_value

    def get_action_selection(self):
        alpha = -self.winning_value
        beta = self.winning_value

        actions = self.board_manager.get_action_list()
        best_evaluation = -float("inf")
        best_actions = []
        print(f'Number of actions to process: {len(actions)}')
        for i, action in enumerate(actions):
            next_board_state = self.board_manager.get_successor(action=action)
            action_eval = self.min_value(next_board_state, alpha, beta)
            print(f'{self} - Processing action: {str(action):40} Evaluation: {action_eval:5.1f}; {(i+1)/(len(actions))*100:.1f}% complete.')

            if action_eval >= beta:
                return action
            if action_eval > best_evaluation:
                best_evaluation = action_eval
                best_actions.clear()
            if action_eval >= best_evaluation:
                best_actions.append(action)

            alpha = max(alpha, best_evaluation)

        rand_index = random.randint(0, len(best_actions) - 1)
        return best_actions[rand_index]

    def max_value(self, board_state, alpha, beta, current_depth=1):
        if current_depth >= self.max_depth or board_state.determine_winner() is not None:
            if self.is_white:
                return board_state.evaluate_state()
            else:
                return -board_state.evaluate_state()

        value = -float("inf")
        actions = board_state.get_action_list()
        for action in actions:
            next_board_state = self.board_manager.get_successor(board_state, action)
            value = max(value, self.min_value(next_board_state, alpha, beta, current_depth + 1))
            if value >= beta:
                return value
            alpha = max(value, alpha)
        return value

    def min_value(self, board_state, alpha, beta, current_depth=1):
        if current_depth >= self.max_depth or board_state.determine_winner() is not None:
            if self.is_white:
                return board_state.evaluate_state()
            else:
                return -board_state.evaluate_state()

        value = float("inf")
        actions = board_state.get_action_list()
        for action in actions:
            next_board_state = self.board_manager.get_successor(board_state, action)
            value = min(value, self.max_value(next_board_state, alpha, beta, current_depth + 1))
            if value <= alpha:
                return value
            beta = min(value, beta)
        return value


class ExpectimaxAI(MinimaxAI):

    def __init__(self, is_white=True, board_manager=None, max_depth=4):
        super().__init__(is_white, board_manager, max_depth)
        self.name = f'Expectimax AI with Depth {self.max_depth}'

    def min_value(self, board_state, alpha, beta, current_depth=1):
        return self.expected_value(board_state, alpha, beta, current_depth)

    def expected_value(self, board_state, alpha, beta, current_depth=1):
        if current_depth >= self.max_depth or board_state.determine_winner() is not None:
            if self.is_white:
                return board_state.evaluate_state()
            else:
                return -board_state.evaluate_state()

        sum_of_values = 0
        actions = board_state.get_action_list()
        for action in actions:
            next_board_state = self.board_manager.get_successor(board_state, action)
            sum_of_values += self.max_value(next_board_state, alpha, beta, current_depth + 1)

        return sum_of_values / len(actions)
