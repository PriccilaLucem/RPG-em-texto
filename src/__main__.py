import curses
import time
from destinations.prismeer.city import City
from characters.hero import Hero
from destinations.prismeer import city_menu
from history.history import init_of_the_history
from global_state.global_state import set_exit, should_exit
from util.display_message_log import display_message_log
main_character = Hero()
prismeer = City()

def key_pressed_event(key, message_log: list, stdscr: curses.window):
    """Handle keypress events and log messages."""
    try:
        if key == ord('P') or key == ord('p'):  
            message = "You arrived at Prismeer!"
            message_log.append(message)
            city_menu(prismeer, main_character, stdscr)
        elif key == ord('B') or key == ord('b'):
            message = "Displaying inventory..."
            backpack_content = main_character.show_backpack()
            for line in backpack_content.splitlines():
                message_log.append(line) 

        elif key == 27:  
            message = "Exiting game..."
            set_exit()

    except Exception as e:
        message_log.append(f"Error while processing key press: {e}")


def game_loop(stdscr: curses.window):
    """Main game loop."""
    curses.curs_set(0)  
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    message_log = []

    story_text = "This is the beginning of your journey...\nYou face an unknown adventure.\n"
    story_lines = story_text.splitlines()
    
    message_log.append("Welcome to the game! Press ESC to exit.")

    story_visible = True

    while not should_exit():
        stdscr.clear()

        stdscr.addstr(0, 0, "Game is running...\n")
        stdscr.addstr(1, 0, "Press any key (ESC to exit)...\n")
        stdscr.addstr(2, 0, "    B - View Backpack\n")
        stdscr.addstr(3, 0, "    P - Prismeer\n")

        if story_visible:
                    for line in story_lines:
                        message_log.append(line)  # Adiciona cada linha da história ao message_log
                    message_log.append("Press any key to continue...")
        else:
            message_log.append("Exploration Mode Activated.")
        
        display_message_log(stdscr, message_log)

        stdscr.refresh()

        key = stdscr.getch()

        key_pressed_event(key, message_log, stdscr)

        if key == 27:  
            break

def main(stdscr):
    """Entry point for the curses application."""
    try:
        game_loop(stdscr)
    except KeyboardInterrupt:
        print("Game interrupted.")
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    curses.wrapper(main)
