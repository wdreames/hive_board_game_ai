"""
This file is only used for debugging purposes and custom interactions with the game board and the AI.
This is not meant to be used other than for development purposes.
"""
import copy
import itertools
from multiprocessing import Queue, set_start_method
import random
from timeit import default_timer as timer
from multiprocessing import Array, Process, Lock

import traceback

import numpy as np
import src.game.board as board
import src.agents as agents


class Contestant:
    
    id_iter = itertools.count()
    
    def __init__(self, weights, performance_history=None):
        self.id = next(Contestant.id_iter)
        self.weights = weights
        if performance_history is None:
            self.performance_history = []
        else:
            self.performance_history = performance_history

    def record_result(self, result):
        self.performance_history.append(result)

    def get_performance_value(self):
        self_num_wins = sum([1 if x > 0 else 0 for x in self.performance_history])
        self_num_losses = sum([1 if x < 0 else 0 for x in self.performance_history])
        self_num_draws = len(self.performance_history) - self_num_wins - self_num_losses
        
        win_multiplier = 1.0
        draw_multiplier = 0.25
        loss_multiplier = -1.0

        return win_multiplier * self_num_wins + draw_multiplier * self_num_draws + loss_multiplier * self_num_losses

    def __lt__(self, other):
        # Contestants that win more-often are ranked higher than those that lose more-often
        tie_limit = 2.0
        self_value = self.get_performance_value()
        other_value = other.get_performance_value()
        if abs(self_value - other_value) >= tie_limit:
            return self_value < other_value
        
        # If contestants are close to each other in the number of wins/losses, compare their median performance

        # Lowest ranked contestants lose quickly
        # Highest ranked contestants win quickly
        self_result = np.median(self.performance_history) if self.performance_history else 0
        other_result = np.median(other.performance_history) if other.performance_history else 0
        
        if self_result < 0 and other_result < 0 or self_result > 0 and other_result > 0:
            return self_result > other_result
        
        return self_result < other_result

    def __str__(self):
        return f'Contestant {self.id}:\n\tweights: {self.weights}\n\tperformance_history: {self.performance_history}\n\tmedian_performance: {np.median(self.performance_history)}\n\twinrate_value: {self.get_performance_value()}'


def crossover(parent1, parent2, cross_chance=0.9):
    if random.random() < cross_chance:
        child1 = []
        child2 = []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
    else:
        child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
    
    return child1, child2


def mutate(weights, mutation_chance=0.5, mutation_range=(-0.5, 0.5)):
    for i in range(len(weights)):
        if random.random() < mutation_chance:
            weights[i] += weights[i] * random.uniform(mutation_range[0], mutation_range[1])
    return weights


def get_next_generation_of_weights(contestants_list, mutation_chance=0.5, mutation_range=(-0.5, 0.5), crossover_chance=0.5, chance_of_low_performing_parent=0.2):
    highest_performers = contestants_list[:len(contestants_list)//2]
    lowest_performers = contestants_list[len(contestants_list)//2:]

    parents_weights = []
    for i in range(len(highest_performers)):
        parents_weights.append(highest_performers[i].weights)

    children = []
    for i in range(0, len(parents_weights), 2):
        for child_weights in crossover(parents_weights[i], parents_weights[i+1], crossover_chance):
            children.append(Contestant(mutate(child_weights, mutation_chance, mutation_range)))

    return highest_performers + children


def play_game(minimax_depth, contestant1: Contestant, contestant2: Contestant, results_queue, max_time=float("inf"), max_turns=float("inf")):
    board_manager = board.BoardManager()

    player1 = agents.MinimaxAI(board_manager, max_depth=minimax_depth, is_white=True, weights_override=contestant1.weights)
    player2 = agents.MinimaxAI(board_manager, max_depth=minimax_depth, is_white=False, weights_override=contestant2.weights)

    start_of_game = timer()

    try:
        while board_manager.get_board().determine_winner() is None and board_manager.get_board().turn_number < max_turns:
            time_check = timer()
            if time_check - start_of_game > max_time:
                break

            if board_manager.get_board().is_white_turn():
                chosen_action = player1.get_action()
            else:
                chosen_action = player2.get_action()

            # board_manager.get_board().print_board()
            # print(f'Turn {board_manager.get_board().turn_number}: Performing action {chosen_action}')
            board_manager.perform_action(chosen_action)
    except KeyboardInterrupt:
        pass
    except Exception:
        board_manager.get_board().print_board(hex_board=False)
        board_manager.save_state('last_hive_error.hv')
        print(traceback.format_exc())

    winner = board_manager.get_board().determine_winner()
    num_moves = board_manager.get_board().turn_number
    if winner == board.HiveGameBoard.WHITE_WINNER:
        print(f'Contestant {contestant1.id} (white) won against contestant {contestant2.id} (black) after {num_moves} moves.')
        contestant1.record_result(num_moves)
        contestant2.record_result(-num_moves)
    elif winner == board.HiveGameBoard.BLACK_WINNER:
        print(f'Contestant {contestant2.id} (black) won against contestant {contestant1.id} (white) after {num_moves} moves.')
        contestant1.record_result(-num_moves)
        contestant2.record_result(num_moves)
    else:
        print(f'Contestant {contestant1.id} (white) drew against contestant {contestant2.id} (black) after {num_moves} moves.')
        contestant1.record_result(0)
        contestant2.record_result(0)
    results_queue.put(contestant1)
    results_queue.put(contestant2)


def run_games_in_thread(thread_name, contestants, minimax_depth, results_queue, max_time=float("inf"), max_turns=float("inf")):
    for i in range(0, len(contestants), 2):
        contestant1 = contestants[i]
        contestant2 = contestants[i+1]
        print(f'Starting {thread_name} game {i // 2 + 1}: Contestant {contestant1.id} (white) vs Contestant {contestant2.id} (black)')
        play_game(minimax_depth, contestant1, contestant2, results_queue, max_time=max_time, max_turns=max_turns)
    print(f'Completed games for {thread_name}')
    

def run_tournament(num_threads=4, minimax_depth=1, num_iterations=10, num_contestants=10, mutation_chance=0.5, mutation_range=(-0.5, 0.5), crossover_chance=0.5):
    initial_weights = get_initial_weights()
    contestants = [Contestant(weights=mutate(copy.deepcopy(initial_weights), mutation_chance, mutation_range)) for _ in range(num_contestants)]

    for i in range(num_iterations):
        print(f'Beginning iteration {i+1} of the tournament.')
        random.shuffle(contestants)
        results_queue = Queue(maxsize=len(contestants))

        # Setup each game of the tournament in its own thread
        group_size = num_contestants // num_threads
        split_contestants = [contestants[i:i + group_size] for i in range(0, len(contestants), group_size)]
        
        num_games_per_thread = len(split_contestants[0])//2
        print(f'Starting {len(split_contestants)} threads with {num_games_per_thread} games per thread.')

        threads = []
        for i, thread_contestants in enumerate(split_contestants):
            max_time = 60
            max_turns = 250
            thread_name = f'thread_{i}'
            threads.append(Process(target=run_games_in_thread, name=thread_name, args=(thread_name, thread_contestants, minimax_depth, results_queue, max_time, max_turns)))
        
        # Run all of the games
        for thread in threads:
            print(f'Starting {thread.name}')
            thread.start()
        for thread in threads:
            print(f'Waiting for {thread.name} to join')
            thread.join(timeout=65 * num_games_per_thread)
            print(f'Closed {thread.name}')
        
        results_list = []
        while not results_queue.empty():
            results_list.append(results_queue.get())

        # Results have been updated. Sort the winner and losers lists by the number of moves taken to win
        sorted_results = sorted(results_list, reverse=True)
        
        print()
        print('Results:')
        for i, contestant in enumerate(sorted_results):
            print(f'{i+1}) {contestant}')
        print()
        contestants = get_next_generation_of_weights(sorted_results, mutation_chance, mutation_range, crossover_chance)

        print(f'New set of contestant ids: {[contestant.id for contestant in contestants]}')


def get_initial_weights():
    return [np.float64(30.094167858236915), np.float64(26.412187154142785), np.float64(16.752860830825192), np.float64(-12.815439648609516), np.float64(-2.4785431422982778), np.float64(2.5089565839894954), np.float64(2.5), np.float64(1.8214369192215634), np.float64(18.902250096728874), np.float64(3.396090957595242), np.float64(-27.930221086526867), np.float64(-21.037339548922024), np.float64(-17.5), np.float64(16.964811734850706), np.float64(2.452836928503475), np.float64(-3.3500699715936095), np.float64(-3.240902481397448), np.float64(-2.422114284233539), np.float64(-40.19134370433577), np.float64(-2.8479827270219067)]


if __name__ == '__main__':
    run_tournament(num_threads=6, minimax_depth=1, num_iterations=60, num_contestants=12, mutation_chance=0.5, mutation_range=(-0.2, 0.2), crossover_chance=0.9)

"""
Initial weights:
[ 25.   17.5  17.5 -17.5  -2.5   2.5   2.5   2.5  27.5   2.5 -25.  -17.5
 -17.5  17.5   2.5  -2.5  -2.5  -2.5 -27.5  -2.5]

Run 1 (depth=1, num_contestants=24, mutation_chance=0.5, mutation_range=(-0.2, 0.2), crossover_chance=0.75):
Completed iteration 15. Best num moves required to win: 30. Best set of weights:
[ 17.84422163  25.50722389  19.50353302 -20.71853605  -2.81849083
   2.32619991   2.09205938   1.34467075  34.03166069   2.38018812
 -17.38420258 -10.85456027 -14.74209535  22.1014505    3.87493485
  -3.62362199  -1.65266801  -2.242204   -24.54052899  -3.21392307]
  
Run 2 (depth=1, num_contestants=12, mutation_chance=0.5, mutation_range=(-0.2, 0.2), crossover_chance=0.75):
Completed iteration 10. Best num moves required to win: 25. Best set of weights:
[ 26.06950448  17.41335848  19.19934669 -13.02920856  -2.60593164
   1.84814204   3.03269643   3.3256608   26.31312606   1.93410642
 -26.70902123 -14.50474529 -11.89436101  17.05782949   2.75299588
  -1.82199723  -2.31487787  -2.10847871 -31.79581841  -2.93312666]

Run 3 - started with previous final results (depth=1, num_contestants=12, mutation_chance=0.5, mutation_range=(-0.2, 0.2), crossover_chance=0.75)
Completed iteration 15. Best num moves required to win: 26. Best set of weights:
[ 36.14419617  17.75095498  15.70920424 -16.86175759  -2.24627586
   2.75309735   4.81458776   2.92088099  27.01602935   1.64046421
 -25.60508446 -14.77552603 -18.6019402   13.85979065   3.6630406
  -2.01350739  -2.20729211  -1.16702621 -15.95284149  -2.64535017]
  
Run 4 - improved algorithm - started with original weights (minimax_depth=1, num_contestants=12, mutation_chance=0.5, mutation_range=(-0.2, 0.2), crossover_chance=0.9)
Contestant 17:
        weights:     [np.float64(27.6086870419417), np.float64(24.656183012421167), np.float64(17.5), np.float64(-16.85305425352481), np.float64(-2.2782412378479764), np.float64(2.9495115156162215), np.float64(2.5), np.float64(2.121575982323753), np.float64(22.100181072044343), np.float64(2.7611359983011488), np.float64(-23.192327895713017), np.float64(-18.82498587894583), np.float64(-17.5), np.float64(15.445537695088444), np.float64(2.6158721593537515), np.float64(-2.8260170757324485), np.float64(-2.8136942296538017), np.float64(-2.4270805006143954), np.float64(-31.769964844327884), np.float64(-2.5)]
        performance: [28, 0, 45, 37, -32, 0, 36, 0, 51]
        
Run 5 - starting with weights from previous run (minimax_depth=1, num_contestants=12, mutation_chance=0.5, mutation_range=(-0.2, 0.2), crossover_chance=0.9)
Contestant 0:
        weights:     [np.float64(27.6086870419417), np.float64(27.551949910590476), np.float64(16.752860830825192), np.float64(-13.73953692207899), np.float64(-2.6752240910205463), np.float64(3.134236656109911), np.float64(2.5), np.float64(2.121575982323753), np.float64(22.100181072044343), np.float64(3.0883141218416568), np.float64(-23.192327895713017), np.float64(-18.82498587894583), np.float64(-17.5), np.float64(16.004938856208618), np.float64(2.6158721593537515), np.float64(-2.8260170757324485), np.float64(-2.8136942296538017), np.float64(-2.520594554094963), np.float64(-37.44168087466862), np.float64(-2.4656962891586494)]
        performance: [35, 54, 0, 42, 30, 45, 40, -40, -42, 46, 38, 53, 45, 0, 46, -40, 44]
2) Contestant 114:
        weights:     [np.float64(29.151710063161158), np.float64(24.656183012421167), np.float64(15.477974480995272), np.float64(-15.064530984141035), np.float64(-2.482213542210385), np.float64(2.666266356495119), np.float64(2.7899402851148167), np.float64(1.904099260512566), np.float64(26.04979853646893), np.float64(3.377891962166726), np.float64(-33.15997006872793), np.float64(-22.844621355184334), np.float64(-14.737808229305466), np.float64(19.517074970135404), np.float64(3.3449110603471244), np.float64(-2.8788540917431016), np.float64(-2.475383309635197), np.float64(-2.8524511771504297), np.float64(-34.755179186303856), np.float64(-2.432620964331362)]
        performance: [36, 27, 34, -109, 46, -54, -34, 32, -28, 34, -52, 0]

Run 6 - starting with run 5 contestant 0 weights (minimax_depth=1, num_contestants=12, mutation_chance=0.5, mutation_range=(-0.2, 0.2), crossover_chance=0.9)
Contestant 16:
        weights:     [np.float64(30.094167858236915), np.float64(26.412187154142785), np.float64(16.752860830825192), np.float64(-12.815439648609516), np.float64(-2.4785431422982778), np.float64(2.5089565839894954), np.float64(2.5), np.float64(1.8214369192215634), np.float64(18.902250096728874), np.float64(3.396090957595242), np.float64(-27.930221086526867), np.float64(-21.037339548922024), np.float64(-17.5), np.float64(16.964811734850706), np.float64(2.452836928503475), np.float64(-3.3500699715936095), np.float64(-3.240902481397448), np.float64(-2.422114284233539), np.float64(-40.19134370433577), np.float64(-2.8479827270219067)]
        performance: [45, 58, 0, 33, 38, 34, 0, 0, 37, 0, 48, -42, 0, 33, -60, 38, 0, 68, 46, -47, -38, -41, -42, 47, -36, 28, 36, 34, 35]
        performance_value: 10.5
        
Run 7 - starting with run 6 contestant 16 weights (minimax_depth=1, num_contestants=12, mutation_chance=0.5, mutation_range=(-0.2, 0.2), crossover_chance=0.9)

"""
