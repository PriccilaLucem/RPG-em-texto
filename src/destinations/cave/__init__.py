from destinations.cave.owl_bear_cave import OwlBearCave
from characters.hero import Hero
from global_state.global_state import should_exit, set_exit
from commands_allowed import cave_commands
import curses
from util.display_message import display_message

def cave(owl_bear_cave: OwlBearCave, main_character: Hero, stdscr: curses.window) -> None:
    curses.curs_set(0)

    actions = {
        chr(10): lambda: display_message(stdscr, "Entering cave...", 1000),
        "B": lambda: display_message(stdscr, f"Displaying inventory...\n{main_character.show_inventory()}", 1000),
        "E": lambda: display_message(stdscr, "Returning to previous menu...", 1000) or exit_loop(),
        chr(27): lambda: display_message(stdscr, "Exiting the game...", 1000) or set_exit()
    }

    def exit_loop():
        raise StopIteration
            

    while not should_exit():
        try:
            stdscr.clear()
            stdscr.addstr(cave_commands())
            stdscr.refresh()

            owl_bear_cave_key = stdscr.getch()

            action = actions.get(chr(owl_bear_cave_key).upper(), lambda: display_message(stdscr, "Invalid choice. Try again.", 1000)) 
            action()
        except StopIteration:
            break
        except Exception as e:   
            handle_error(stdscr, e)

def display_inventory(main_character: Hero, stdscr: curses.window) -> None:

    inventory = main_character.show_inventory()
    display_message(stdscr, f"Displaying inventory...\n{inventory}", 1000)

def handle_error(stdscr: curses.window, e: Exception) -> None:

    display_message(stdscr, f"An error occurred: {e}", 2000)
