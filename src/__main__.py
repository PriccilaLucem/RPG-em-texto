import curses
from destinations.prismeer.city import City
from characters.hero import Hero
from destinations.prismeer import CityMenu
from history.history import init_of_the_history
from global_state.global_state import should_exit, update_game_state, get_game_state
from util.display_message import display_message, draw_menu
from destinations.cave.owl_bear_cave import OwlBearCave
from destinations.cave import OutsideCave
from destinations.forest.forest import Forest
from destinations.forest import ForestMenu
from menu.menu import Menu


def key_pressed_event(stdscr: curses.window, allow_enter_cave: bool, hero: Hero, prismeer: City, owl_bear_cave: OwlBearCave, wood_forest: Forest, atual_location: str, menu: Menu):
    """Handles key press events and triggers corresponding actions."""
    menu.is_in_game = True
    city_menu = CityMenu(prismeer, hero, stdscr, menu)
    forest_menu = ForestMenu(wood_forest, hero, stdscr, menu)
    cave_menu = OutsideCave(owl_bear_cave, hero, stdscr, menu)
    if atual_location != "menu" or atual_location != "prismeer surroundings":
        if atual_location == "prismeer":
            city_menu.run()
        elif atual_location == "forest":
            forest_menu.run()
        elif atual_location == "cave":
            cave_menu.run()
    
    # Define key actions based on menu options
    key_actions = {
        "Menu": lambda: menu.run(),  # Open the main menu
        "Prismeer": lambda: city_menu.run(),  # Go to Prismeer
        "Forest": lambda: forest_menu.run(),  # Go to the Forest
        "Owl Bear Cave": lambda: cave_menu.run()  # Go to the OwlBear Cave
    }

    update_game_state(hero=hero, prismeer=prismeer, cave=owl_bear_cave, forest=wood_forest, atual_location="prismeer_surroundings")

    try:
        selected_index = 0
        while True:
            # Render the UI
            render_ui(stdscr, allow_enter_cave, selected_index)

            # Get user input
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = max(0, selected_index - 1)
            elif key == curses.KEY_DOWN:
                menu_options = get_menu_options(allow_enter_cave)
                selected_index = min(len(menu_options) - 1, selected_index + 1)
            elif key == ord('\n'):  # Enter key
                menu_options = get_menu_options(allow_enter_cave)
                selected_option = menu_options[selected_index]
                action = key_actions.get(selected_option, lambda: display_message(stdscr, "Invalid choice. Try again.", 1000))
                action()
                break
    except Exception as e:
        display_message(stdscr, f"Error while processing key press: {e}", 1000)


def get_menu_options(allow_enter_cave: bool) -> list:
    """Returns a list of menu options with their corresponding action keys."""
    menu_options = [
        "Menu",
        "Prismeer",
        "Forest"
    ]
    if allow_enter_cave:
        menu_options.append("Owl Bear Cave")
    return menu_options


def render_ui(stdscr: curses.window, allow_enter_cave: bool, selected_index: int):
    """Renders the game UI with the selected menu option highlighted."""
    stdscr.clear()
    menu_options = get_menu_options(allow_enter_cave)
    draw_menu(stdscr, "Game is running...", menu_options, selected_index)
    stdscr.refresh()

def game_loop(stdscr: curses.window, hero: Hero, prismeer: City, owl_bear_cave: OwlBearCave, wood_forest: Forest):
    """Main game loop."""
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    menu = Menu(stdscr, prismeer, False)
    menu.run()

    game_state = get_game_state()
    if game_state["is_new_game"]:
        history = init_of_the_history()
        display_message(stdscr, history, 5000)
        update_game_state(is_new_game=False)
        atual_location = "prismeer_surroundings"
    else:
        hero, prismeer, owl_bear_cave, wood_forest, atual_location = (
            game_state["hero"],
            game_state["prismeer"],
            game_state["cave"],
            game_state["forest"],
            game_state["atual_location"]
        )

    while not should_exit():
        allow_enter_cave = any(
            quest.id == 1
            for quest in (hero.quests or []) + (hero.concluded_quests or [])
        )
        key_pressed_event(stdscr, allow_enter_cave, hero, prismeer, owl_bear_cave, wood_forest, atual_location, menu)


def main(stdscr):
    """Initializes the game and starts the main loop."""
    hero = Hero()
    prismeer = City()
    owl_bear_cave = OwlBearCave()
    forest = Forest()
    update_game_state(hero=hero, prismeer=prismeer, cave=owl_bear_cave, forest=forest)

    try:
        game_loop(stdscr, hero, prismeer, owl_bear_cave, forest)
    except KeyboardInterrupt:
        print("Game interrupted.")
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    curses.wrapper(main)