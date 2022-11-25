import src.game.board as board


# TODO: Add documentation
def make_choice(description, prompt, choices):
    exit_options = {'quit', 'exit', 'q'}

    print(description)
    for i, choice in enumerate(choices):
        print(f'{i + 1}: {choice}')

    selection = input(prompt)
    if selection.lower() in exit_options:
        return _save_and_exit(description, prompt, choices)
    elif not selection.isnumeric() or int(selection) not in range(1, len(choices) + 1):
        return make_choice(description, prompt, choices)

    return choices[int(selection) - 1]


def _save_and_exit(last_description, last_prompt, last_choices):
    # Confirm save and exit
    confirm_exit = make_choice(
        'Are you sure you want to exit the game?',
        'Select an option:',
        ['Yes', 'No']
    )
    if confirm_exit != 'Yes':
        return make_choice(last_description, last_prompt, last_choices)

    # Determine save location
    print('Where would you like to save your game? The game will be saved under the `data` directory.')
    file_name = input('Enter a name for the save file. Default is "last_hive_game.hv": ')
    if file_name:
        board.BoardManager().save_state(file_name)
    else:
        board.BoardManager().save_state()
    exit(0)


def add_to_dict_set(dictionary, key, value):
    """
    This is a helper function used to add values to sets stored within a dictionary.

    :param dictionary:
    :param key:
    :param value:
    """
    if key in dictionary:
        dictionary[key].add(value)
    else:
        dictionary[key] = {value}
