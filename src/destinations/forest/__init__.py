# from characters.MainCharacter import MainCharacter
# from global_state.global_state import should_exit, set_exit
# from util.display_message import display_message, draw_menu
# from destinations.forest.forest import Forest
# import curses

# class ForestMenu:
#     def __init__(self, forest: Forest, MainCharacter: MainCharacter, stdscr: curses.window, menu) -> None:
#         self.forest = forest
#         self.MainCharacter = MainCharacter
#         self.stdscr = stdscr
#         self.menu = menu
#         self.message_log = [
#             "Welcome to the Forest!",
#             "You can gather resources, check your status, or return to Prismeer.",
#         ]
#         self.menu_options = [
#             "Menu",
#             "Gather Resources",
#             "Exit Forest",
#         ]
#         self.selected_index = 0

#     def run(self) -> None:
#         """Main loop for the forest menu."""
#         curses.curs_set(0)  

#         while not should_exit():
#             try:
#                 self.draw_menu()
#                 self.handle_input()
#             except StopIteration:
#                 break
#             except Exception as e:
#                 display_message(self.stdscr, f"An error occurred: {e}", 2000)

#     def draw_menu(self) -> None:
#         """Draws the forest menu."""
#         draw_menu(self.stdscr, "Forest Actions", self.menu_options, self.selected_index)

#     def handle_input(self) -> None:
#         """Handles user input for the forest menu."""
#         key = self.stdscr.getch()

#         if key == curses.KEY_UP:
#             self.selected_index = max(0, self.selected_index - 1)
#         elif key == curses.KEY_DOWN:
#             self.selected_index = min(len(self.menu_options) - 1, self.selected_index + 1)
#         elif key == ord('\n'):  # Enter key
#             self.handle_menu_option(self.menu_options[self.selected_index])

#     def handle_menu_option(self, option: str) -> None:
#         if option == "Menu":
#             self.menu.run()           
#         elif option == "Gather Resources":  # Gather Resources
#             self.forest.search_for_resources(self.stdscr, self.MainCharacter)
#             self.message_log.append("Gathered resources.")
#         elif option == "Exit Forest":  # Exit Forest
#             display_message(self.stdscr, "Returning to Prismeer surroundings...", 1000)
            
#             raise StopIteration  # Exit the loop