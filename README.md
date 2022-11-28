# Hive Board Game AI

William Reames\
December 2nd, 2022

This is the capstone for my BS in Computer Science degree from Christopher Newport University. This is still a work in progress

The goal of this project is to create an AI for the board game, *Hive*. More information about the board game can be found [here](https://boardgamegeek.com/boardgame/2655/hive)

## Installation Prerequisites:
2. Install Python (https://www.python.org/downloads/)
3. Install pip (https://pip.pypa.io/en/stable/installation/)
4. Run `# pip install virtualenv` on the command line

## Installation and Setup
1. Clone the git repository to your local machine:

`# git clone https://github.com/wdreames/hive_board_game_ai.git`

2. Move into the downloaded directory

`# cd hive_board_game_ai`

3. Create a virtual environment

`# virtualenv env`

4. Activate the environment

`# source ./env/bin/activate`

5. Install the necessary requirements

`# pip install -r requirements.txt`

6. Give the play_hive.sh file executable permissions

`# chmod 755 play_hive.sh`

## Playing The Game

After completing the steps above, run the following commands from within the `hive_board_game_ai` directory whenever you would like to play the game:

1. `# source ./env/bin/activate`
2. `# ./play_hive.sh`

Run `# ./play_hive.sh --help` to learn how to load previously saved games or change the size of the board to fit your screen.
