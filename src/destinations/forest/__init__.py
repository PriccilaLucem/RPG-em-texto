from characters.hero import Hero
from global_state.global_state import should_exit, set_exit
from util.display_message import display_message
from destinations.forest.forest import Forest
import curses

def exit_loop():
    raise StopIteration

def forest(regular_forest: Forest, main_character: Hero, stdscr: curses.window, menu) -> None:
    curses.curs_set(0)

    actions = {
        "S": lambda: main_character.show_status(stdscr),
        "E": lambda: display_message(stdscr, "Returning to prismeer surroundings", 1000) or exit_loop(),
        "G": lambda: regular_forest.search_for_resources(stdscr, main_character),
        chr(27): lambda: display_message(stdscr, "Exiting the game...", 1000) or set_exit(),
    }

    while not should_exit():
        try:
            stdscr.clear()
            stdscr.addstr("Forest Actions:\n")
            stdscr.addstr("    S - View Status\n")
            stdscr.addstr("    G - Gather Resources\n")
            stdscr.addstr("    E - Exit Forest\n")
            stdscr.addstr("    ESC - Exit Game\n")
            stdscr.refresh()

            forest_key = stdscr.getch()

            action = actions.get(chr(forest_key).upper(), lambda: display_message(stdscr, "Invalid choice. Try again.", 1000))
            action()
        except StopIteration:
            break
        except Exception as e:
            display_message(stdscr, f"An error occurred: {e}", 2000)
