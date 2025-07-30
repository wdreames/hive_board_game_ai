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
        self.recent_game_limit = 9
        self.weights = weights
        if performance_history is None:
            self.performance_history = []
        else:
            self.performance_history = performance_history

    def record_result(self, result):
        self.performance_history.append(result)

    def get_recent_performance_history(self):
        if len(self.performance_history) > self.recent_game_limit:
            return self.performance_history[-self.recent_game_limit:]
        return self.performance_history[:]

    def get_performance_value(self):
        recent_performance_values = self.get_recent_performance_history()
        
        # An even length of performance values would cause the middle two values to be averaged, which messes up the sorting algorithm
        if recent_performance_values and len(recent_performance_values) % 2 == 0:
            recent_performance_values.pop()
        return np.median(recent_performance_values) if recent_performance_values else 0

    def get_winrate_value(self):
        recent_performance_values = self.get_recent_performance_history()
        self_num_wins = sum([1 if x > 0 else 0 for x in recent_performance_values])
        self_num_losses = sum([1 if x < 0 else 0 for x in recent_performance_values])
        self_num_draws = len(recent_performance_values) - self_num_wins - self_num_losses
        
        win_multiplier = 1.0
        draw_multiplier = -0.25
        loss_multiplier = -1.0

        return win_multiplier * self_num_wins + draw_multiplier * self_num_draws + loss_multiplier * self_num_losses

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError(f"Class {self.__class__} is not comparable with {other.__class__}.")
        
        # Contestants that win more-often are ranked higher than those that lose more-often
        tie_limit = 2.0
        self_value = self.get_winrate_value()
        other_value = other.get_winrate_value()
        if abs(self_value - other_value) >= tie_limit:
            return self_value < other_value
        
        # If contestants are close to each other in the number of wins/losses, compare their median performance

        # Lowest ranked contestants lose quickly
        # Highest ranked contestants win quickly
        self_result = self.get_performance_value()
        other_result = other.get_performance_value()
        
        if self_result < 0 and other_result < 0 or self_result > 0 and other_result > 0:
            return self_result > other_result
        
        return self_result < other_result

    def __str__(self):
        return f'Contestant {self.id}:\n\tweights: {self.weights}\n\tperformance_history: {self.performance_history}\n\tmedian_performance: {self.get_performance_value()}\n\twinrate_value: {self.get_winrate_value()}'


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


def play_game(minimax_depth, contestant1: Contestant, contestant2: Contestant, results_queue, max_time_per_move=float("inf"), max_time_per_game=float("inf"), max_turns_per_game=float("inf")):
    board_manager = board.BoardManager()

    player1 = agents.MinimaxAI(board_manager, max_depth=minimax_depth, max_time=max_time_per_move, is_white=True, weights_override=contestant1.weights)
    player2 = agents.MinimaxAI(board_manager, max_depth=minimax_depth, max_time=max_time_per_move, is_white=False, weights_override=contestant2.weights)

    start_of_game = timer()

    try:
        while board_manager.get_board().determine_winner() is None and board_manager.get_board().turn_number < max_turns_per_game:
            time_check = timer()
            if time_check - start_of_game > max_time_per_game:
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

def run_games_in_thread(thread_name, contestants, minimax_depth, results_queue,  max_time_per_move=float("inf"), max_time_per_game=float("inf"), max_turns_per_game=float("inf")):
    for i in range(0, len(contestants), 2):
        contestant1 = contestants[i]
        contestant2 = contestants[i+1]
        print(f'Starting {thread_name} game {i // 2 + 1}: Contestant {contestant1.id} (white) vs Contestant {contestant2.id} (black)')
        play_game(minimax_depth, contestant1, contestant2, results_queue, max_time_per_move=max_time_per_move, max_time_per_game=max_time_per_game, max_turns_per_game=max_turns_per_game)
    print(f'Completed games for {thread_name}')
    

def run_tournament(num_threads=4, minimax_depth=1, num_iterations=10, num_contestants=10, mutation_chance=0.5, mutation_range=(-0.5, 0.5), crossover_chance=0.5, max_time_per_move=float("inf"), max_time_per_game=float("inf"), max_turns_per_game=float("inf")):
    initial_weights = get_initial_weights()
    contestants = [Contestant(initial_weights)] + [Contestant(weights=mutate(copy.deepcopy(initial_weights), mutation_chance, mutation_range)) for _ in range(num_contestants - 1)]

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
            thread_name = f'thread_{i}'
            threads.append(Process(target=run_games_in_thread, name=thread_name, args=(thread_name, thread_contestants, minimax_depth, results_queue, max_time_per_move, max_time_per_game, max_turns_per_game)))
        
        # Run all of the games
        for thread in threads:
            print(f'Starting {thread.name}')
            thread.start()
        for thread in threads:
            print(f'Waiting for {thread.name} to join')
            thread.join(timeout=max_time_per_game * num_games_per_thread + 5)
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
    return [1,1,1,1,1,1,1,1,1,1]
    return [482.0995973399494, 3.2242430892810825, 27.7235511309986, -0.48336047759406564, -0.22454442284522128, 0.14364161231710681, 0.2771940489184473, -0.020682666521378124, 14.16321981398211, 0.06365532306114718]

if __name__ == '__main__':
    run_tournament(num_threads=6, minimax_depth=1, num_iterations=2500, num_contestants=12, mutation_chance=0.5, mutation_range=(-1.5, 1.5), crossover_chance=0.9, max_time_per_move=60, max_time_per_game=300, max_turns_per_game=100)

"""
Original weights:
[25.0, 17.5, 17.5, -17.5, -2.5, 2.5, 2.5, 2.5, 27.5, 2.5, -25.0, -17.5, -17.5, 17.5, 2.5, -2.5, -2.5, -2.5, -27.5, -2.5]

Original weights for white only:
[25.0, 17.5, 17.5, -17.5, -2.5, 2.5, 2.5, 2.5, 27.5, 2.5]

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

<Improved genetic algorithm>

Run 4 - started with original weights (minimax_depth=1, num_contestants=12, mutation_chance=0.5, mutation_range=(-0.2, 0.2), crossover_chance=0.9)
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
Contestant 1:
        weights: [np.float64(30.094167858236915), np.float64(24.69409496206863), np.float64(18.77756520733354), np.float64(-12.815439648609516), np.float64(-2.4785431422982778), np.float64(2.5089565839894954), np.float64(2.5), np.float64(1.7333191512906276), np.float64(18.902250096728874), np.float64(3.343768130870377), np.float64(-27.930221086526867), np.float64(-21.037339548922024), np.float64(-17.5), np.float64(16.964811734850706), np.float64(2.760003489637841), np.float64(-3.313298413049461), np.float64(-3.6213119724867595), np.float64(-2.422114284233539), np.float64(-38.00374557042221), np.float64(-2.8479827270219067)]
        performance_history: [29, 0, 51, 0, 35, 0, 36, 30, -57, 51, -60, 40, -40, 37, 42, 37, 109, -46, 73, 0, -36, 0, 0, 0, 37, -51, 0, 0, 53, 32, 0, 73, -41, 42, -46, 0, 28, -36, 0, -52, 51, -29, 39, -37, -40, 38, 50, 0, 33, -43, 59, 61, 0, 111, 0, 37, -50, 0, 0, 0]
        median_performance: 0.0
        winrate_value: 16.5
Contestant 55:
        weights: [np.float64(26.333082006078904), np.float64(24.69409496206863), np.float64(18.77756520733354), np.float64(-15.33591498601253), np.float64(-2.4565397317615716), np.float64(2.98189933395701), np.float64(2.7822392180148494), np.float64(1.7070112463085145), np.float64(22.37962548680019), np.float64(3.7151801655868772), np.float64(-29.015848368193257), np.float64(-21.037339548922024), np.float64(-17.5), np.float64(13.902419200425266), np.float64(2.760003489637841), np.float64(-3.829327491195521), np.float64(-3.6462431969540257), np.float64(-2.422114284233539), np.float64(-44.6109732693211), np.float64(-3.270936194605737)]
        performance_history: [27, 61, 47, 0, 30, 42, -36, 0, 0, 27, 0, -34, 0, 39, 0, 59, -37, -51, 34, -32, 35, 84, 36, -73, -48, 0, 0, 0, 51, 43, 0, -48, 0, 31, 49, -33, 34, -51, -53, 39, -33, -35, -36, 0, 0, 89, 0, 37, 50, -26, 0, 29]
        median_performance: 0.0
        winrate_value: 10.75

Run 8 - starting with run 7 contestant 1 weights (minimax_depth=1, num_contestants=12, mutation_chance=0.75, mutation_range=(-2.0, 2.0), crossover_chance=1.0)
Contestant 9:
        weights: [np.float64(29.576873358847287), np.float64(3.570441535573721), np.float64(33.38357490410702), np.float64(-12.815439648609516), np.float64(1.7994150115517695), np.float64(4.016696371193444), np.float64(7.347061005026117), np.float64(1.7333191512906276), np.float64(14.472793338699397), np.float64(2.547248952979537), np.float64(-27.930221086526867), np.float64(-14.921580667572778), np.float64(5.287864855973076), np.float64(-4.473638762527418), np.float64(1.1567712915392645), np.float64(1.8838266177188476), np.float64(-10.385528515221413), np.float64(-4.394292187305705), np.float64(-38.00374557042221), np.float64(-1.8136596734974093)]
        performance_history: [34, 0, 28, 52, 26, 0, 0, 52, 0, -38, 36, 31, 56, 28, 0, 58, -24, -36, 30, 0, 36, 0, 0, 0, 28, -24, -36, 32, 0, 32, 34, 52, -36, 0, 0, 80, 34, -34, -24, 0, -54, -30, 48, 0, -32, 30, 46, 46, -34, 0, 41, 0, -38, 0, 0, 0, 72, -37, -26, 0, 0, -30, 44, 30, 51, -130, -28, 102, 0, 40, 22, 24, 26, 0, 52, 0, -28, -41, -28, 66, 58, -92, -32, 30, -26, -32, 40, -40, 0, 0, 0, 0, 58, 42, -30, 28, -72, -30, 0, 39, -28, 48, 0, 28, -38, 49, -42, 0, 36, 54, 0, 26, 0, 0, 0, 32, 45, 0, -27, 37]
        median_performance: 0.0
        winrate_value: 27.0
Contestant 7:
        weights: [np.float64(30.094167858236915), np.float64(24.69409496206863), np.float64(38.65544074057753), np.float64(9.677125889466325), np.float64(1.458428265683593), np.float64(5.620330571516392), np.float64(-2.221329255579354), np.float64(3.8221526541449053), np.float64(18.902250096728874), np.float64(1.0143079689470302), np.float64(-27.930221086526867), np.float64(-21.037339548922024), np.float64(-17.5), np.float64(16.964811734850706), np.float64(1.9012551489042933), np.float64(-5.655450704606622), np.float64(-3.6213119724867595), np.float64(-3.4646591337938286), np.float64(-38.00374557042221), np.float64(-2.8479827270219067)]
        performance_history: [42, -30, 40, 0, 0, 50, 48, 50, 0, -50, 38, 37, 45, 0, 137, 0, 24, -51, 83, 0, 45, 0, 32, 0, 27, 0, 54, -32, 24, 0, 42, -52, 33, 96, 0, 0, 34, 30, 24, 30, 33, 0, 33, 28, 32, 0, -31, 0, -105, 33, 0, 34, 42, 26, 41, -35, -30, 25, 36, 33, 142, 0, 29, 32, 29, 130, 76, 42, 0, 38, 45, 26, -32, 49, 28, 27, 28, 41, 47, 30, 38, -48, 33, 65, 26, 29, 22, 33, -54, 34, 0, 0, 33, -42, -34, 58, 27, 0, 32, 44, 28, 27, -37, 33, 30, 44, 29, 0, -36, 48, 21, 0, 0, 33, 25, -50, 0, 0, 27, 23]
        median_performance: 28.0
        winrate_value: 66.5
Contestant 74:
        weights: [np.float64(42.6720966886826), np.float64(68.0881053020472), np.float64(15.030158410036055), np.float64(-32.1318598113364), np.float64(1.2681917725589829), np.float64(2.404194037786449), np.float64(8.080945742203593), np.float64(4.676779733826326), np.float64(38.33064470266952), np.float64(-0.796880166178335), np.float64(-27.930221086526867), np.float64(-17.690999909934625), np.float64(-13.532669182439102), np.float64(16.964811734850706), np.float64(-3.7415982632028983), np.float64(-5.655450704606622), np.float64(-0.11305399933739269), np.float64(-2.7514329782644795), np.float64(-101.64582320647523), np.float64(-2.8479827270219067)]
        performance_history: [36, 0, 28, 52, 65, 89, 68, -27, 29, 0, 57, 0, 34, 28, 0, -38, 0, 53, -36, 0, -36, 45, 38, 28, 51, -34, 0, 41, -36, 53, 24, 39, 0, 33, 0, 43, 34, 105, 0, 0, 42, 26, 0, 28, 0, 34, 54, 48, 0, 0, -29, -44, -35, 0, 44, 43, 0, 32, 0, 55, 42, 32, 0, 43, 38, 48, 62, 29, 43, -58, 0, 0, 41, -44, 32, -32, 0, 0, 70, 28, 31, 31, 48, 34, 0, -32, 0, 0, 35, 37, 38, 56, 48, 34, -40, 28, 0, 0, -30, 40, 30, 0, 0, 0, 0, 36, -38, 42, 24]
        median_performance: 28.0
        winrate_value: 53.0
Contestant 623:
        weights: [np.float64(79.26429491394595), np.float64(10.212183095512021), np.float64(6.416654725314942), np.float64(-33.32977147116328), np.float64(4.635540850907265), np.float64(4.613712726990379), np.float64(23.929826474468488), np.float64(3.8208798197867058), np.float64(26.2449061056007), np.float64(0.19077710782307922), np.float64(-1.4711654612411034), np.float64(-15.137846811470055), np.float64(13.356588668027413), np.float64(0.2571729543218614), np.float64(-3.7415982632028983), np.float64(-0.5325762288917395), np.float64(1.6746572524293177), np.float64(1.8758352018139517), np.float64(-79.93458246498582), np.float64(2.772226328009082)]
        performance_history: [36, 30, 24, 40, 32, 0, 26, 44, 0, 26, 0, -33, 32, 0, 28, 0, 28, 26]
        median_performance: 26.0
        winrate_value: 12.25

<Improved contestant ranking algorithm>

Run 9 - starting with run 8 contestant 623 weights (minimax_depth=1, num_contestants=12, mutation_chance=0.75, mutation_range=(-2.0, 2.0), crossover_chance=1.0)
Contestant 183:
        weights: [np.float64(211.86214999348664), np.float64(-3.2403211582583724), np.float64(89.05825873969944), np.float64(0.1509215893224376), np.float64(2.0659551449533704), np.float64(0.0665799435909375), np.float64(35.422230022818056), np.float64(-15.764814333986925), np.float64(0.5759882344539604), np.float64(0.003535441311417536), np.float64(-1.3620262526242919), np.float64(1.3470938184515617), np.float64(-17.602619948246833), np.float64(-2.733188214038032), np.float64(-0.18788479635928118), np.float64(0.322148012589218), np.float64(7.541101872523516), np.float64(12.38572242492311), np.float64(-7.622983599332699), np.float64(0.04997074132680712)]
        performance_history: [52, 48, 34, 24, 0, 36, -27, 0, 30, -42, 0, 0, 32, -36]
        median_performance: 0
        winrate_value: -1.0
1) Contestant 235:
        weights: [np.float64(91.8828269560276), np.float64(-8.51079246797461), np.float64(65.67409700681958), np.float64(0.15370788689127907), np.float64(2.0659551449533704), np.float64(0.16777223270874234), np.float64(35.422230022818056), np.float64(-21.344225894740454), np.float64(0.3694360460681012), np.float64(-0.001814748297130128), np.float64(-1.3620262526242919), np.float64(1.3470938184515617), np.float64(-0.6040979922140719), np.float64(0.12453524823112772), np.float64(-0.4208148092370113), np.float64(-0.24364814088444137), np.float64(-0.47794176254536025), np.float64(22.16194544582693), np.float64(-7.622983599332699), np.float64(0.04997074132680712)]
        performance_history: [26, 32, 39, -36, -56, 23]
        median_performance: 26
        winrate_value: 2.0

Run 10 - starting with the original weights for white only (black weights are mirrored) (minimax_depth=1, num_contestants=12, mutation_chance=0.75, mutation_range=(-2.0, 2.0), crossover_chance=1.0)
Contestant 9:
        weights: [61.34454583049565, 1.129816781464502, 39.559924688171606, 13.63758535320229, 0.4318128176568803, -1.458744110920711, 5.682561804211629, 3.201565383558962, 29.46342547908396, 2.5]
        performance_history: [33, 81, 54, 80, 48, 30, 42, 42, 50, 34, 41]
        median_performance: 42.0
        winrate_value: 9.0
Contestant 118:
        weights: [482.0995973399494, 3.2242430892810825, 96.79139592805792, -0.48336047759406564, -0.03084497704606408, -0.35647194025252293, 12.954282518228828, 44.7177261010208, 27.16321981398211, 4.360513378033113]
        performance_history: [30, 54, 30, 30, 44, 36, 29]
        median_performance: 30.0
        winrate_value: 7.0
Contestant 203:
        weights: [417.62947922704745, -4.009421117113153, 66.0953459264619, 0.9820633525428213, -0.03289645597484092, -7.548694963415399, 0.1857165602725429, -8.49966337755462, 1.9749402327268584, -0.07543227295385808]
        performance_history: [41, 32, 48, 28, 0, 40, 0, 26]
        median_performance: 32.0
        winrate_value: 5.5

Run 11 - starting with a mix of run 10 contestant 118 and 203 (num_threads=6, minimax_depth=2, num_iterations=500, num_contestants=12, mutation_chance=0.60, mutation_range=(-2.0, 2.0), crossover_chance=1.0, max_time_per_move=200, max_time_per_game=200*80, max_turns_per_game=80)
Contestant 10:
        weights: [482.0995973399494, 3.2242430892810825, 27.7235511309986, -0.48336047759406564, -0.22454442284522128, 0.14364161231710681, 0.2771940489184473, -0.020682666521378124, 14.16321981398211, 0.06365532306114718]
        performance_history: [39, 0, 34, 53, 37, -31, 43, 40, 45, 43, 64, -37]
        median_performance: 43.0
        winrate_value: 5.0
        
Run 12 - starting with run 11 contestant 10 weights (num_threads=6, minimax_depth=1, num_iterations=500, num_contestants=12, mutation_chance=0.65, mutation_range=(-0.2, 0.2), crossover_chance=1.0, max_time_per_move=60, max_time_per_game=300, max_turns_per_game=100)
1) Contestant 2961:
        weights: [93.16171905178355, 1.8693734113476352, 52.41911016151369, -0.1682611937055484, -0.08598631104249256, 0.04890283535822403, 0.8904971793978608, -0.03890874507656261, 0.5342486630653795, 0.02823936423603152]
        performance_history: [30, 48, 37, 0, 67, 68, 51, -44]
        median_performance: 48.0
        winrate_value: 4.75
12) Contestant 2909:
        weights: [72.76655736024148, 1.8690176716666302, 27.75059114491946, -0.12844451835197654, -0.11758566386721761, 0.059364698743402645, 0.5986053914476076, -0.03993604455946739, 0.547244273517883, 0.03022447233597878]
        performance_history: [27, 45, 32, 40, 54, 40, -31, 44, 32, -34, -48, 0, 36, 38, 0, 54, -34]
        median_performance: 0.0
        winrate_value: 0.5

Run 13 - starting with `1` for all weights (num_threads=6, minimax_depth=1, num_iterations=388, num_contestants=12, mutation_chance=0.65, mutation_range=(-0.2, 0.2), crossover_chance=0.9, max_time_per_move=60, max_time_per_game=300, max_turns_per_game=100)
Contestant 2314:
        weights: [2.0727174466777187, 0.43062314768168175, 0.5868187988918447, 0.17904632263694878, 0.5213094996223167, 0.26697540985825124, 0.3361533719818756, 0.2466300405825513, 0.19519153225200592, 0.37616328082467476]
        performance_history: [37, 46, 36]
        median_performance: 37.0
        winrate_value: 3.0
Contestant 2270:
        weights: [2.4571522591696295, 0.6279773684729827, 0.7538968242372678, 0.16959383467111389, 0.47927057921815547, 0.3034965494096136, 0.38366439658118945, 0.368215590482877, 0.22112068806919982, 0.517780053350381]
        performance_history: [70, 48, 0, 0, 59, -56, 41, 0, 34, -43]
        median_performance: 0.0
        winrate_value: 1.25

# I realized the above set of hyperparameters prevents negative weights from being formed. Adjusted the mutation range to fix that.
Run 14 - starting with `1` for all weights (num_threads=6, minimax_depth=1, num_iterations=2500, num_contestants=12, mutation_chance=0.5, mutation_range=(-1.5, 1.5), crossover_chance=0.9, max_time_per_move=60, max_time_per_game=300, max_turns_per_game=100)

"""
