# Game Statistics

### Runs from 11/15/2022 on my Local Machine

Using branch: player_ui \
This file contains data produced after running a series of games 
as a certain AI.

| AI Type           | Num Runs | Avg Time Per Turn | Avg Num Actions | Avg Num Actions on a Turn |
|-------------------|----------|-------------------|-----------------|---------------------------|
| best_next_move_ai | 10       | 0.164730          | 34              | 42                        |
| best_next_move_ai | 10       | 0.112711          | 26.8            | 39                        |
| minimax_ai1       | 10       | 0.508682          | 33.9            | 43                        |
| minimax_ai1       | 10       | 0.813650          | 35.4            | 50                        |
| minimax_ai1       | 5        | 0.571237          | 21.2            | 37                        |
| expecitmax_ai1    | 5        | 3.156283          | 35.8            | 47                        |
| expecitmax_ai1    | 5        | 2.354916          | 25.4            | 42                        |
| expecitmax_ai1    | 5        | 2.328763          | 24.6            | 43                        |

Using branch : player_ui \
Changed to 0 pts for allied pieces around queen bee. 1 pt for movable pieces throughout whole game

| AI Type           | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| best_next_move_ai | 10       | 0.142122          | 35            | 45                        | 938                                 |
| minimax_ai1       | 10       | 0.972560          | 28.2          | 44                        | 4250                                |
| expectimax_ai1    | 5        | 2.817311          | 23.8          | 42                        | 15405                               |
| minimax_ai2       | 1        | 92.181857         | 50.0          |                           | 1379327                             |
| minimax_ai2       | 2        | 50.017008         | 38.5          | 43                        | 197811                              |


### Runs from 11/16/2022 on Google VM

Using branch: board_manager

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 1        | 0.224344          | 22.0          |                           | 3756                                |
| minimax_ai1 | 1        | 0.381149          | 30.0          |                           | 6485                                |
| minimax_ai1 | 1        | 0.252298          | 18.0          |                           | 2884                                |
| minimax_ai1 | 1        | 0.443863          | 26.0          |                           | 4567                                |
| minimax_ai1 | 1        | 0.254693          | 26.0          |                           | 3977                                |
| minimax_ai2 | 1        | 46.090381         | 24.0          |                           | 616063                              |
| minimax_ai2 | 1        | 10.396830         | 18.0          |                           | 107373                              |
| minimax_ai2 | 1        | 50.820059         | 27.0          |                           | 801546                              |


Using branch: player_ui

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 1-25     | 1.159315          | 38.3          | 49                        | 5156                                |
| minimax_ai2 | 1        | 72.03995          | 50+           |                           | 1651536                             |

Reverted to max/min functions from board_manager

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 16/25    | 0.316752          | 34.2          | 49                        | 2947                                |

Reverted to the get_action_selection function from board_manager

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 17/25    | 0.373708          | 37.8          | 45                        | 4160                                |

Reverted to eval function from board_manager

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 13/25    | 0.400160          | 38.9          | 43                        | 2809                                |

Changed the eval function

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 7/10     | 0.324168          | 35.2          | 40                        | 3426                                |

Less value for pieces that can move to QB

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 8/10     | 0.312562          | 33.4          |                           | 3785                                |

Running on branch board_manager again with updated main.py

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 8/10     | 0.330422          | 30.8          |                           | 3817                                |


### Runs from 11/25/2022 on my Local Machine

Sorted actions and updated eval function

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 9/10     | 1.037267          | 30.6          |                           | 6385                                |

Negative points for immovable pieces; 0 points for movable ones.

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 5/5      | 0.671093          | 27.6          |                           | 3798                                |

Immovable allied pieces around the allied QB hold 80% value.
Also changed exponential value from 1.5 to 1.2

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 3/5      | 0.725731          | 37.8          |                           | 2744                                |

Changed exponential value back from 1.2 to 1.5

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 5/5      | 0.681309          | 27.2          |                           | 3814                                |

More discouragement of placing pieces

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 5/5      | 0.728307          | 32.2          |                           | 4871                                |

I played against the same AI, and it was *significantly* more aggressive than before. I'm going to remove piece 
discouragement for pieces that are around the queen bee now and see what happens.

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai1 | 5/5      | 0.669227          | 27.0          |                           | 3481                                |

This put *way* too much focus on surrounding the queen bee rather than controlling the board.

Went back to the previous version (where it still counts pieces around the qb), and it beat me on a depth of 2!

### Runs from 11/27/2022 on my Local Machine

Improved time-limited minimax

| AI Type                    | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|----------------------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai2 (limit of 10s) | 1/1      | 8.416197          | 55.0          |                           | 100556                              |
| minimax_ai2 (limit of 10s) | 1/1      | 7.452857          | 35.0          |                           | 85913                               |
| minimax_ai2 (limit of 10s) | 1/1      | 6.620348          | 21.0          |                           | 66054                               |
| minimax_ai2 (limit of 10s) | 1/1      | 7.436458          | 51.0          |                           | 72128                               |
| minimax_ai1                | 5/5      | 0.404361          | 24.0          |                           | 2359                                |
| expectimax_ai1             | 5/5      | 3.302013          | 24.4          |                           | 18074                               |

Fixed action list sorting. Now it should always find a pre-sorted list if it finds the same set of actions

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai2 | 1/1      | 8.119532          | 19.0          |                           | 43229                               |
| minimax_ai2 | 0/1      | 84.738074         | 24.0          |                           | 495375                              |


### Runs from 11/27/2022 on Google VM

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai2 | 2/2      | 30.910182         | 35.5          | 42                        | 376761                              |

Results from a game:
```commandline
Total number of actions: 47
Total game time: 959.4865298740042
Average time per action: 20.414607018595834
Average Time Taken by White: 9.752704373449492e-05
Average Time Taken by Black: 41.712697295390726

Number of actions for each object:
Ant             Total Number of Actions:   396477
Beetle          Total Number of Actions:   380299
Grasshopper     Total Number of Actions:   148186
Queen Bee       Total Number of Actions:   32344
Spider          Total Number of Actions:   58477
Average times for each object action:
Ant             Average Time:   0.000528
Beetle          Average Time:   0.000345
Grasshopper     Average Time:   0.000458
Queen Bee       Average Time:   0.000489
Spider          Average Time:   0.000500
Total times for each object action:
Ant             Total Time:      209.367964
Beetle          Total Time:      131.363902
Grasshopper     Total Time:      67.933395
Queen Bee       Total Time:      15.818589
Spider          Total Time:      29.236961

Total number of actions:    1015783
Average across all actions: 0.000447
Total action times:         453.720811

Average time taken to undo an action: 0.000437887691185282
Total time taken to undo actions: 444.7787297814648

Average time taken to create an action list: 2.161362260892869e-05
Total time taken to create an action list: 3.588207171043905
==================================================

Results after 2 games:
White wins: 0 / Black wins: 2 / Draws: 0
Average number of turns per game: 35.5


Average time taken by White across all games: 0.000092
Average time taken by Black across all games: 30.910182
Average number of actions on a turn: 42
Average number of actions processed in a game: 376761
```


Old piece priority:       Q, B, G, S, A\
Reordered piece priority: Q, S, G, B, A

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai2 | 1/1      | 6.722418          | 15.0          | 29                        | 62729                               |
| minimax_ai2 | 1/1      | 28.989206         | 37.0          | 50                        | 494460                              |

Results from games:
```commandline
Total number of actions: 15
Total game time: 47.08000144199468
Average time per action: 3.1386667627996454
Average Time Taken by White: 6.417542837360608e-05
Average Time Taken by Black: 6.722417797425545

Number of actions for each object:
Ant             Total Number of Actions:   15913
Beetle          Total Number of Actions:   30445
Grasshopper     Total Number of Actions:   6387
Queen Bee       Total Number of Actions:   1700
Spider          Total Number of Actions:   8284
Average times for each object action:
Ant             Average Time:   0.000383
Beetle          Average Time:   0.000345
Grasshopper     Average Time:   0.000318
Queen Bee       Average Time:   0.000365
Spider          Average Time:   0.000420
Total times for each object action:
Ant             Total Time:      6.092408
Beetle          Total Time:      10.488438
Grasshopper     Total Time:      2.033661
Queen Bee       Total Time:      0.619852
Spider          Total Time:      3.475689

Total number of actions:    62729
Average across all actions: 0.000362
Total action times:         22.710047

Average time taken to undo an action: 0.0003414637965698999
Total time taken to undo actions: 21.414902001881273

Average time taken to create an action list: 1.3689573989119586e-05
Total time taken to create an action list: 0.2543933534398093
==================================================

Results after 1 game:
White wins: 0 / Black wins: 1 / Draws: 0
Average number of turns per game: 15.0


Average time taken by White across all games: 0.000064
Average time taken by Black across all games: 6.722418
Average number of actions on a turn: 29
Average number of actions processed in a game: 62729
==================================================
```

```commandline
Total number of actions: 37
Total game time: 521.8782579639956
Average time per action: 14.104817782810692
Average Time Taken by White: 8.048711040626383e-05
Average Time Taken by Black: 28.989205653945344

Number of actions for each object:
Ant             Total Number of Actions:   216179
Beetle          Total Number of Actions:   36739
Grasshopper     Total Number of Actions:   53870
Queen Bee       Total Number of Actions:   14537
Spider          Total Number of Actions:   173135
Average times for each object action:
Ant             Average Time:   0.000481
Beetle          Average Time:   0.000317
Grasshopper     Average Time:   0.000466
Queen Bee       Average Time:   0.000350
Spider          Average Time:   0.000599
Total times for each object action:
Ant             Total Time:      103.898540
Beetle          Total Time:      11.637818
Grasshopper     Total Time:      25.077500
Queen Bee       Total Time:      5.082271
Spider          Total Time:      103.747982

Total number of actions:    494460
Average across all actions: 0.000504
Total action times:         249.444112

Average time taken to undo an action: 0.0004971937560748083
Total time taken to undo actions: 245.8488881475787

Average time taken to create an action list: 1.9993840894327033e-05
Total time taken to create an action list: 2.571647803510132
==================================================

Results after 1 game:
White wins: 0 / Black wins: 1 / Draws: 0
Average number of turns per game: 37.0


Average time taken by White across all games: 0.000080
Average time taken by Black across all games: 28.989206
Average number of actions on a turn: 50
Average number of actions processed in a game: 494460
==================================================

```

## Runs from 11/27/2022 on my Local Machine

Changed sorting of actions so min_value sorts low to high

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai2 | 1/1      | 31.524069         | 21.0          | 43                        | 140117                              |


## Runs from 11/27/2022 on Google VM

| AI Type     | Num Runs | Avg Time Per Turn | Avg Num Turns | Avg Num Actions on a Turn | Avg Num Actions Processed in a Game |
|-------------|----------|-------------------|---------------|---------------------------|-------------------------------------|
| minimax_ai2 | 1/1      | 17.315905         | 26.0          | 38                        | 225683                              |
