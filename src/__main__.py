import curses
import time
from threading import Event
from destinations.prismeer.city import City
from characters.hero import Hero
from destinations.prismeer import city_menu
from history.history import init_of_the_history
from commands_allowed import game_init
from global_state.global_state import set_exit, should_exit

main_character = Hero()
prismeer = City()


def key_pressed_event(key, message_log: list, story_visible: dict):
    """Handle keypress events and log messages."""
    try:
        if key == ord('P') or key == ord('p'):  
            message = "You arrived at Prismeer!"
            message_log.append(message)
            story_visible["visible"] = False  # Hide the story
        elif key == ord('B') or key == ord('b'):
            message = "Displaying inventory..."
            message_log.append(message)
        elif key == 27:  
            message = "Exiting game..."
            message_log.append(message)
            set_exit()

    except Exception as e:
        message_log.append(f"Error while processing key press: {e}")


def display_message_log(stdscr: curses.window, message_log: list):
    """Display the message log at the bottom of the screen."""
    h, w = stdscr.getmaxyx()  
    log_start_line = h - len(message_log) - 1

    for i, message in enumerate(message_log[-(h - 2):]):  
        stdscr.addstr(log_start_line + i, 0, message[:w]) 


def main_game_loop(stdscr: curses.window):
    # Configure the curses window
    stdscr.nodelay(False)  # Make getch blocking for proper key detection
    stdscr.keypad(True)  # Enable keypad input for special keys

    message_log = []  # Initialize the message log
    story_visible = {"visible": True}  # Track whether the story should be displayed

    # Retrieve the story text
    story_text = init_of_the_history()
    story_lines = story_text.splitlines()

    while True:
        stdscr.clear()

        # Display static content
        stdscr.addstr(0, 0, "Game is running...\n")
        stdscr.addstr(1, 0, "Press any key (ESC to exit)...\n")
        stdscr.addstr(2, 0, game_init())
        # Conditionally display the story (persistent content)
        if story_visible["visible"]:
            for i, line in enumerate(story_lines, start=3):
                stdscr.addstr(i, 0, line)

        # Display the message log at the bottom
        display_message_log(stdscr, message_log)

        stdscr.refresh()

        # Handle user input
        try:
            c = stdscr.getch()  # Wait for user input
            if c == 27:  # ESC key
                message_log.append("Exiting game...")
                break
            elif c != -1:
                key_pressed_event(c, message_log, story_visible)

        except Exception as e:
            message_log.append(f"Error while processing key press: {e}")

        time.sleep(0.1)  # Small delay for smoother loop execution


def main(stdscr):
    """Entry point for the curses application."""
    try:
        main_game_loop(stdscr)
    except KeyboardInterrupt:
        print("Game interrupted.")
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    curses.wrapper(main)
