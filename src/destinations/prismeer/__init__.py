from destinations.prismeer.city import City
from characters.main_character import MainCharacter
from global_state.global_state import should_exit, get_game_state, update_game_state, exit_loop
from util.display_message import display_message, draw_menu, draw_menu_with_history
from destinations.prismeer.comercial_center import Comercial_center 
from menu.menu import Menu
from history.damon_history import damon_history
import curses

class CityMenu:
    def __init__(self, city: City, main_character: MainCharacter, stdscr: curses.window, menu:Menu) -> None:
        self.city_center = CityCenter(city, MainCharacter, stdscr, menu)
        self.city = city
        self.stdscr = stdscr
        self.menu = menu
        self.main_character = main_character
        self.message_log = [
            "Welcome to Prismeer!",
            "You can visit the city center, check the billboard, or rest at the inn.",
        ]
        self.menu_options = [
            "Menu",
            "Exit the city",
            "See the billboard",
            "Rest at the inn",
            "Go to bar",
            "Go to the center",
        ]
        self.selected_index = 0

    def run(self) -> None:
        atual_location = get_game_state()["atual_location"]
        if atual_location == "prismeer_center":
            self.city_center.run()
        if atual_location not in ["prismeer", "prismeer_center"]:
            return
        
        


        while not should_exit():
            update_game_state(prismeer=self.city, main_character=self.main_character, atual_location="prismeer")
            damon_history_start = get_game_state().get("damon_history_start")
            if not damon_history_start:
                options = ["Follow Damon"]
                index = 0
                while True:
                    draw_menu_with_history(self.stdscr, "=== You finally meet Damon ===", damon_history(), options, index)
                    key = self.stdscr.getch()
                    if key == 10:
                        self.city.bar.bar_menu(self.main_character, self.city.damon)
            try:
                self.draw_menu()
                self.handle_input()
            except StopIteration:
                break
            except Exception as e:
                display_message(self.stdscr, f"An error occurred: {e}", 2000)

    def draw_menu(self) -> None:
        """Draws the city menu."""
        draw_menu(self.stdscr, "Welcome to Prismeer", self.menu_options, self.selected_index)

    def handle_input(self) -> None:
        """Handles user input for the city menu."""
        key = self.stdscr.getch()

        if key == curses.KEY_UP:
            self.selected_index = max(0, self.selected_index - 1)
        elif key == curses.KEY_DOWN:
            self.selected_index = min(len(self.menu_options) - 1, self.selected_index + 1)
        elif key == ord('\n'):  # Enter key
            self.handle_menu_option(self.menu_options[self.selected_index])

    def handle_menu_option(self, option: str) -> None:
        """Handles the selected menu option."""
        if option.startswith("Go to bar"): # Go to bar
            self.city.bar.bar_menu(self.stdscr, self.main_character)
        if option.startswith("See the billboard"):  # See the billboard
            self.city.billboard.billboard_menu()
        elif option.startswith("Rest at the inn"):  # Rest at the inn
            self.city.inn.pass_the_night(self.main_character, self.stdscr)
        elif option.startswith("Menu"):
            self.menu.run()
        elif option.startswith("Go to the center"):  # Go to the center
            update_game_state(atual_location="prismeer_center")
            self.city_center.run()
        elif option.startswith("Exit the city"):  # Exit the city
            display_message(self.stdscr, "Leaving Prismeer...", 1000, curses.color_pair(11))
            exit_loop("prismeer_surroundings")

class CityCenter:
    def __init__(self, city: 'City', main_character: MainCharacter, stdscr: curses.window, menu) -> None:
        self.city = city
        self.main_character = main_character
        self.stdscr = stdscr
        self.downtown: Comercial_center  = get_game_state().get("comercial_center") or Comercial_center(stdscr)

        self.menu = menu
        self.menu_options = [
            "Show Menu",
            "Exit to city menu",
            "Visit the armor shop",
            "Visit the weapon shop",
            "Talk to Afrac",
            "Talk to Osvaldo",
            "Talk to Damon",
            "Talk to blacksmith",
        ]
        self.selected_index = 0

    def run(self) -> None:
        """Main loop for the city center menu."""
        atual_location = get_game_state()["atual_location"]
        if atual_location != "prismeer_center":
            return

        curses.curs_set(0)
        update_game_state(prismeer=self.city, main_character=self.main_character, prismeer_downtown=self.downtown)

        while not should_exit():
            try:
                self.draw_menu()
                self.handle_input()
            except StopIteration:
                break
            except Exception as e:
                display_message(self.stdscr, f"An error occurred: {e}", 2000)

    def draw_menu(self) -> None:
        """Draws the city center menu with improved styling."""
        draw_menu(self.stdscr, "Welcome to the City Center", self.menu_options, self.selected_index)

    def handle_input(self) -> None:
        """Handles user input for the city center menu."""
        key = self.stdscr.getch()

        if key == curses.KEY_UP:
            self.selected_index = max(0, self.selected_index - 1)
        elif key == curses.KEY_DOWN:
            self.selected_index = min(len(self.menu_options) - 1, self.selected_index + 1)
        elif key == ord('\n'):  # Enter key
            option = self.menu_options[self.selected_index]
            if option == "Visit the armor shop":  # Visit the armor shop
                self.downtown.armor_shop.shop_interactions(self.main_character)
            elif option == "Visit the weapon shop":  # Visit the weapon shop
                self.downtown.weapon_shop.shop_interactions( self.stdscr)
            elif option == "Talk to blacksmith":  # Talk to blacksmith
                self.downtown.talk_to_blacksmith(self.stdscr, self.main_character)
            elif option == "Exit to city menu":  # Exit to city menu
                display_message(self.stdscr, "Returning to city menu...", 1000, curses.color_pair(11))
                exit_loop("prismeer")
            elif option == "Show Menu":  # Show Menu
                self.menu.run()
            elif option == "Talk to Afrac":  # Talk to Afrac
                self.talk_to_npc(1, "Afrac")
            elif option == "Talk to Osvaldo":  # Talk to Osvaldo
                self.talk_to_npc(2, "Osvaldo")
            elif option == "Talk to Damon":  # Talk to Damon
                self.talk_to_npc(3, "Damon")

    def talk_to_npc(self, npc_id: int, npc_name: str) -> None:
        npc_response = self.downtown.talk_to_npc(npc_id, self.main_character)
        display_message(self.stdscr, f"{npc_name}: {npc_response}", 2000, curses.color_pair(1))

        if npc_id == 3 and self.downtown.npcs[2].quest is not None:
            self.handle_quest_offer(npc_id, npc_name)

    def handle_quest_offer(self, npc_id: int, npc_name: str) -> None:
        """Handles a quest offer from an NPC with improved styling."""
        display_message(self.stdscr, f"{npc_name} offered a quest.", 2000, curses.color_pair(1))

        options = ["Accept the quest", "Deny the quest"]
        selected_index = 0

        while True:
            draw_menu(self.stdscr, "Quest Offer", options, selected_index)
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif key == 10:  # Tecla ENTER
                if selected_index == 0:  # Aceitar missão
                    self.downtown.append_npc_quest(self.main_character, npc_id)
                    display_message(self.stdscr, "Quest Accepted!", 1500, curses.color_pair(1))
                else:  # Recusar missão
                    display_message(self.stdscr, "Quest Denied.", 1500, curses.color_pair(1))
                break