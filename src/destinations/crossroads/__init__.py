import curses
from global_state.global_state import get_game_state, update_game_state, exit_loop
from util.display_message import draw_menu_with_history, draw_menu
from history.history import crossroads_history, the_mistery_of_crossroads
from typing import TYPE_CHECKING
from destinations.prismeer import CityMenu
from destinations.nitna_village import NitnaMenu

if TYPE_CHECKING:
    from characters.main_character import MainCharacter
    from destinations.prismeer.city import City
    from menu.menu import Menu

class CrossRoads:
    def __init__(self, main_character: "MainCharacter", city: "City", nitna, stdscr: curses.window, menu: "Menu"):
        self.main_character = main_character
        self.prismeer = city
        self.stdscr = stdscr
        self.menu = menu
        self.nitna = nitna
        self.options = [
            "Open Menu",
            "Go to Prismeer",
            "Go to the forest",
            "Go to Nitna Village",
        ]
        self.selected_index = 0

    def run(self):
        """Main game loop for crossroads location"""
        game_state = get_game_state()
        atual_location = game_state.get("atual_location")

        # Handle cases where player isn't at crossroads
        if atual_location != "crossroads":
            self.handle_non_crossroads_location(atual_location)
            return
        
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)   
        options = ["Continue"]
        index = 0
        if not game_state.get("saw_intro_crossroads"):
            update_game_state(saw_intro_crossroads = True)
            self.show_intro("===THE SOUND OF THE BIRDS===", crossroads_history(), options, index)
            self.show_intro("===THE SECRETS OF CROSSROADS===", the_mistery_of_crossroads(), options, index, curses.color_pair(10))
        while True:
            try:
                update_game_state(main_character=self.main_character, prismeer=self.prismeer)
                self.draw()
                key = self.stdscr.getch()
                self.handle_input(key)
            except StopIteration:
                break
            
    def handle_non_crossroads_location(self, location: str):
        """Redirect to appropriate location handler"""
        city_center = CityMenu(self.prismeer, self.main_character, self.stdscr, self.menu)
        nitna_village = NitnaMenu(self.nitna, self.stdscr, self.main_character, self.menu)

        if location in ["city_center", "prismeer"]:
            city_center.run()
        elif location in ["forest", "owl_bear_cave"]:
            pass  # TODO: Add forest handling
        elif location == "nitna_village":
           nitna_village.run()

    def show_intro(self, title, crossroads_history, options, index, color_pair= None):
        """Display introductory message for crossroads"""
        while True:
            draw_menu_with_history(self.stdscr, title, crossroads_history, options, index, color_pair)
            key = self.stdscr.getch()
            if key == 10:  
                break

    def draw(self):
        """Draw the crossroads menu"""
        draw_menu(self.stdscr, "CROSSROADS", self.options, self.selected_index)

    def handle_input(self, key):
        """Handle player input"""
        if key == curses.KEY_UP:
            self.selected_index = max(0, self.selected_index - 1)
        elif key == curses.KEY_DOWN:
            self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
        elif key == 10:  # Enter key
            self.execute_option()

    def execute_option(self):
        """Execute selected menu option"""
        option = self.options[self.selected_index]

        if option == "Go to Prismeer":
            exit_loop(atual_location="prismeer")
        elif option == "Go to the forest":
            exit_loop(atual_location="forest")            
        elif option == "Go to Nitna Village":
            exit_loop(atual_location="nitna_village")
            
        elif option == "Open Menu":
            self.menu.run()