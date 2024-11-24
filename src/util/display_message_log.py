import curses
def display_message_log(stdscr: curses.window, message_log: list):
    """
    Displays a scrollable message log at the bottom of the screen.
    
    Args:
        stdscr (curses.window): The curses window where the log is displayed.
        message_log (list): A list of strings representing log messages.
    """
    max_y, max_x = stdscr.getmaxyx()

    log_start_line = max(6, max_y - len(message_log) - 1)

    visible_messages = message_log[-(max_y - log_start_line - 1):]

    for idx, msg in enumerate(visible_messages):
        line = log_start_line + idx
        if line < max_y:  
            stdscr.addnstr(line, 0, str(msg), max_x - 1)
