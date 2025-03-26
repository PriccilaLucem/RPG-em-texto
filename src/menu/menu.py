import curses
from util.save_game import load_game_and_update, save_game
from util.display_message import display_message, draw_menu
from global_state.global_state import update_game_state, get_game_state, should_exit
from util.status import show_status
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from characters.main_character import MainCharacter
    
class Menu:
    def __init__(self, stdscr: curses.window, is_in_game=False):
        self.stdscr = stdscr
        self.main_character = None
        self.is_in_game = is_in_game
        self.in_game_options =  ["Show Status", "Close Menu", "Save Game", "Load Game", "Exit Game"]
        self.menu_options = ["New Game", "Load Game", "Exit Game"]
        self.selected_index = 0

    def exit_game(self):
        self.stdscr.clear()
        self.stdscr.addstr("Exiting the game...\n", curses.A_BOLD)
        self.stdscr.refresh()
        curses.napms(1000)
        exit(0)

    def close_menu(self):
        raise StopIteration

    def execute_option(self):
        options = self.in_game_options if self.is_in_game else self.menu_options
        selected_option = options[self.selected_index]

        if selected_option == "Close Menu":
            self.close_menu()
        elif selected_option == "Show Status":
            show_status(self.main_character, self.stdscr)
        elif selected_option == "Save Game":
            save_game(self.stdscr)
            self.close_menu()
        elif selected_option == "Load Game":
            game_state = load_game_and_update(self.stdscr)
            if not game_state:
                return False
            else:
                update_game_state(**game_state)
                self.main_character = game_state.get("main_character", self.main_character)
            self.close_menu()
        elif selected_option == "Exit Game":
            self.exit_game()
        elif selected_option == "New Game":
            self.close_menu()
        else:
            display_message(self.stdscr, "Invalid choice. Try again.", 1000)

    def run(self):
        while not should_exit():
            try:
                self.main_character = get_game_state().get("main_character")
                self.is_in_game = get_game_state()["is_in_game"]
                options = self.in_game_options if self.is_in_game else self.menu_options
                draw_menu(self.stdscr, "=== Game Menu ===", options, self.selected_index)
                
                key = self.stdscr.getch()
                if key == curses.KEY_UP:
                    self.selected_index = max(0, self.selected_index - 1)
                elif key == curses.KEY_DOWN:
                    self.selected_index = min(len(options) - 1, self.selected_index + 1)
                elif key == ord('\n'):
                    if not self.execute_option():
                        continue
            except StopIteration:
                break
            except Exception as e:
                display_message(self.stdscr, f"An error occurred: {e}", 2000)
