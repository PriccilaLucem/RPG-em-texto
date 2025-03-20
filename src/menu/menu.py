import curses
from util.save_game import load_game_and_update, save_game
from util.display_message import display_message
from global_state.global_state import update_game_state, should_exit
from util.status import show_status

class Menu:
    def __init__(self, stdscr: curses.window, hero, is_in_game=False):
        self.stdscr = stdscr
        self.hero = hero
        self.is_in_game = is_in_game
        self.options = [
            "Close Menu",
            "Show Status",
            "Save Game",
            "Load Game",
            "Exit Game"
        ] if is_in_game else [
            "New Game",
            "Load Game",
            "Exit Game"
        ]
        self.selected_index = 0  # Track the currently selected option

    def exit_game(self):
        self.stdscr.clear()
        self.stdscr.addstr("Exiting the game...\n", curses.A_BOLD)
        self.stdscr.refresh()
        curses.napms(1000)
        exit(0)

    def close_menu(self):
        raise StopIteration

    def render_menu(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Define colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default text
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlighted text
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Title and borders

        # Draw a border around the menu
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.border()
        self.stdscr.attroff(curses.color_pair(3))

        # Draw the title
        title = "=== Game Menu ==="
        self.stdscr.addstr(2, (width - len(title)) // 2, title, curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)

        # Draw the menu options
        for i, option in enumerate(self.options):
            x = (width - len(option)) // 2  # Center the options
            y = 5 + i  # Start below the title
            if i == self.selected_index:
                self.stdscr.addstr(y, x, option, curses.color_pair(2) | curses.A_BOLD)  # Highlight selected option
            else:
                self.stdscr.addstr(y, x, option, curses.color_pair(1))  # Normal option

        # Draw instructions at the bottom
        instructions = "Use UP/DOWN arrows to navigate, ENTER to select, ESC to exit."
        self.stdscr.addstr(height - 2, (width - len(instructions)) // 2, instructions, curses.color_pair(3) | curses.A_BOLD)

        self.stdscr.refresh()

    def execute_option(self):
        """Executa a ação da opção selecionada."""
        selected_option = self.options[self.selected_index]

        if selected_option == "Close Menu":
            self.close_menu()
        elif selected_option == "Show Status":
            show_status(self.hero, self.stdscr)
        elif selected_option == "Save Game":
            save_game(self.stdscr)
            self.close_menu()
        elif selected_option == "Load Game":
            update_game_state(**load_game_and_update(self.stdscr))
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
                self.render_menu()
                key = self.stdscr.getch()

                if key == curses.KEY_UP:
                    self.selected_index = max(0, self.selected_index - 1)  # Move selection up
                elif key == curses.KEY_DOWN:
                    self.selected_index = min(len(self.options) - 1, self.selected_index + 1)  # Move selection down
                elif key == ord('\n'):  # ENTER key
                    self.execute_option()
                elif key == 27:  # ESC key
                    self.close_menu()
                else:
                    continue
            except StopIteration:
                break
            except Exception as e:
                display_message(self.stdscr, f"An error occurred: {e}", 2000)