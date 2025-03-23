exit_game = False 

game_state = {
    "hero": None,
    "prismeer": None,
    "cave": None,
    "forest": None,
    "atual_location": "menu",
    "is_in_game": False,
    "is_new_game": True,
    "combat_done": False,
    "billboard": None,
    "prismeer_downtown": None
}

def update_game_state(**kwargs):
    game_state.update(kwargs)

def get_game_state():
    return game_state

def exit_loop(atual_location):
    update_game_state(atual_location= atual_location)
    raise StopIteration
def set_exit():
    """Set the exit_game flag to True."""
    global exit_game
    exit_game = True

def should_exit():
    """Check if the game should exit."""
    return exit_game
