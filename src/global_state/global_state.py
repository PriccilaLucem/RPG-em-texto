# global_state.py
exit_game = False  # Shared state to track the game's exit status

def set_exit():
    """Set the exit_game flag to True."""
    global exit_game
    exit_game = True

def should_exit():
    """Check if the game should exit."""
    return exit_game
