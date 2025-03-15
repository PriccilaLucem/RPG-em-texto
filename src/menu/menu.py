import curses
from util.save_game import load_game_and_update, save_game
from util.display_message import display_message
from global_state.global_state import update_game_state, should_exit

def exit_game(stdscr: curses.window):
    stdscr.clear()
    stdscr.addstr("Exiting the game...\n", curses.A_BOLD)
    stdscr.refresh()
    curses.napms(1000)
    exit(0)

def close_menu():
    raise StopIteration

def render_menu(stdscr: curses.window, options):
    stdscr.clear()
    stdscr.addstr("=== Game Menu ===\n\n", curses.A_BOLD | curses.A_UNDERLINE)
    
    for key, desc in options.items():
        stdscr.addstr(f"  {key} - {desc}\n")
    
    stdscr.addstr("\nSelect an option: ", curses.A_BOLD)
    stdscr.refresh()

def menu(stdscr: curses.window, main_character, is_in_game=False):

    options = (
        {"Q": "Close Menu","1": "Save Game", "2": "Load Game", "3": "Exit Game","S": "Show Status"} if is_in_game else
        {"1": "New Game", "2": "Load Game", "3": "Exit Game"}
    )

    actions = (
        {
            "1": lambda: save_game(stdscr) or close_menu(),
            "Q": lambda: close_menu(),
            "2": lambda: load_game_and_update(stdscr),
            "3": lambda: exit_game(stdscr),
            "S": lambda: main_character.show_status(stdscr)
        } if is_in_game else
        {
            "1": lambda: close_menu(),
            "2": lambda: load_game_and_update(stdscr),
            "3": lambda: exit_game(stdscr),
        }
    )

    while not should_exit():
        try:
            render_menu(stdscr, options)
            key = stdscr.getch()

            action = actions.get(chr(key).upper(), lambda: display_message(stdscr, "Invalid choice. Try again.", 1000))
            result = action()
            if result:
                update_game_state(**result)
            
                raise StopIteration
        except StopIteration:
            break
        except Exception as e:
            display_message(stdscr, f"An error occurred: {e}", 2000)
