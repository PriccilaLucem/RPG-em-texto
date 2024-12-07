import curses
from destinations.prismeer.city import City
from characters.hero import Hero
from destinations.prismeer import city_menu
from history.history import init_of_the_history
from global_state.global_state import set_exit, should_exit
from util.display_message import display_message
from destinations.cave import cave
from destinations.cave.owl_bear_cave import OwlBearCave

main_character = Hero()
prismeer = City()
owl_bear_cave = OwlBearCave()

def key_pressed_event(key, stdscr: curses.window, allow_enter_cave: bool):
    key_actions = {
        "P": lambda: city_menu(prismeer, main_character, stdscr),
        "E": lambda: display_message(stdscr, "Exiting game...", 0) or set_exit(),
        "C": lambda: cave(owl_bear_cave, main_character, stdscr) if allow_enter_cave else display_message(stdscr, "The cave is not accessible yet.", 1000),
        "S": lambda: main_character.show_status(stdscr),
        chr(27): lambda: display_message(stdscr, "Exiting game...", 0) or set_exit(),  
    }
    
    try:
        action = key_actions.get(chr(key).upper(), lambda: display_message(stdscr, "Invalid choice. Try again.", 1000))
        action()
        
    except Exception as e:
        display_message(stdscr, f"Error while processing key press: {e}", 1000)

def render_ui(stdscr:curses.window, allow_enter_cave):

    stdscr.addstr(0, 0, "Game is running...\n")
    stdscr.addstr(1, 0, "Press any key (ESC to exit)...\n")
    stdscr.addstr(2, 0, "    S - View Status\n")
    stdscr.addstr(3, 0, "    P - Prismeer\n")
    if allow_enter_cave:
        stdscr.addstr(4, 0, "    C - Cave\n")
    stdscr.refresh()

def game_loop(stdscr: curses.window):

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    history = init_of_the_history()
    display_message(stdscr, history, 0)  

    while not should_exit():
        allow_enter_cave = any(
            quest.id == 1
            for quest in (main_character.quests or []) + (main_character.concluded_quests or [])
        )
        render_ui(stdscr, allow_enter_cave)
        key = stdscr.getch()  
        key_pressed_event(key, stdscr, allow_enter_cave)

def main(stdscr):
    
    try:
        game_loop(stdscr)
    except KeyboardInterrupt:
        print("Game interrupted.")
    finally:
        print("Goodbye!")

if __name__ == "__main__":
    curses.wrapper(main)
