import os


DISABLE_LOGS = False
title = ''


def log_title(new_title):
    """
    Change console title message.
    """
    if DISABLE_LOGS:
        return
    title = new_title
    clear_console()
    print(f'\n{title}\n')


def log_subtitle(new_message):
    """
    Change console title message.
    """
    global title
    if DISABLE_LOGS:
        return
    title = f'{title}\n{new_message}'
    clear_console()
    print(f'\n{title}\n')


def log_message(message):
    """
    Change console message.
    """
    if DISABLE_LOGS:
        return
    clear_console()
    print(f'\n{title}\n{message}')


def clear_console():
    """
    Clear all console messages.
    """
    if DISABLE_LOGS:
        return
    command = ''
    if os.name == 'nt':
        command = 'cls'
    else:
        command = 'clear'
    os.system(command)
