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

