from destinations.prismeer.city import City
from characters.hero import Hero
from global_state.global_state import should_exit, set_exit, update_game_state, exit_loop
from util.display_message import display_message, draw_menu

import curses

class CityMenu:
    def __init__(self, city: 'City', main_character: Hero, stdscr: curses.window, menu) -> None:
        self.city = city
        self.main_character = main_character
        self.stdscr = stdscr
        self.menu = menu
        self.message_log = [
            "Welcome to Prismeer!",
            "You can visit the city center, check the billboard, or rest at the inn.",
        ]
        self.menu_options = [
            "Menu",
            "Exit the city",
            "See the billboard",
            "Rest at the inn",
            "Go to the center",
        ]
        self.selected_index = 0

    def run(self) -> None:
        """Main loop for the city menu."""
        curses.curs_set(0)
        update_game_state(prismeer=self.city, hero=self.main_character, atual_location="prismeer")

        while not should_exit():
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
        if option.startswith("See the billboard"):  # See the billboard
            self.city.billboard.billboard_menu(self.stdscr, self.main_character)
            self.message_log.append("Checked the billboard.")
        elif option.startswith("Rest at the inn"):  # Rest at the inn
            self.city.inn.pass_the_night(self.main_character, self.stdscr)
            self.message_log.append("Rested at the inn.")
        elif option.startswith("Go to the center"):  # Go to the center
            city_center = CityCenter(self.city, self.main_character, self.stdscr, self.menu)
            city_center.run()
            self.message_log.append("Visited the city center.")
        elif option.startswith("Exit the city"):  # Exit the city
            display_message(self.stdscr, "Leaving Prismeer...", 1000)
            exit_loop("prismeer_surroundings")
        elif option.startswith("Menu"):  # Show Menu
            self.menu(self.stdscr, self.main_character, is_in_game=True)

class CityCenter:
    def __init__(self, city: 'City', main_character: Hero, stdscr: curses.window, menu) -> None:
        self.city = city
        self.main_character = main_character
        self.stdscr = stdscr
        self.menu = menu
        self.message_log = [
            "Welcome to the City Center!",
            "You can visit shops, talk to NPCs, or return to Prismeer.",
        ]
        self.menu_options = [
            "Show Menu",
            "Visit the armor shop",
            "Visit the weapon shop",
            "Exit to city menu",
            "Talk to Afrac",
            "Talk to Osvaldo",
            "Talk to Damon",
            "Talk to blacksmith",
        ]
        self.selected_index = 0

    def run(self) -> None:
        """Main loop for the city center menu."""
        curses.curs_set(0)
        update_game_state(prismeer=self.city, hero=self.main_character, atual_location="city_center")

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
            self.handle_menu_option(self.menu_options[self.selected_index])

    def handle_menu_option(self, option: str) -> None:
        """Handles the selected menu option."""
        if option == "Visit the armor shop":  # Visit the armor shop
            self.city.downtown.armor_shop.shop_interactions(self.main_character, self.stdscr)
            self.message_log.append("Visited the armor shop.")
        elif option == "Visit the weapon shop":  # Visit the weapon shop
            self.city.downtown.weapon_shop.shop_interactions(self.main_character, self.stdscr)
            self.message_log.append("Visited the weapon shop.")
        elif option == "Talk to blacksmith":  # Talk to blacksmith
            self.city.downtown.talk_to_blacksmith(self.stdscr, self.main_character)
            self.message_log.append("Talked to the blacksmith.")
        elif option == "Exit to city menu":  # Exit to city menu
            display_message(self.stdscr, "Returning to city menu...", 1000)
            exit_loop("city_menu")
        elif option == "Show Menu":  # Show Menu
            self.menu(self.stdscr, self.main_character, True)
        elif option == "Talk to Afrac":  # Talk to Afrac
            self.talk_to_npc(1, "Afrac")
        elif option == "Talk to Osvaldo":  # Talk to Osvaldo
            self.talk_to_npc(2, "Osvaldo")
        elif option == "Talk to Damon":  # Talk to Damon
            self.talk_to_npc(3, "Damon")

    def talk_to_npc(self, npc_id: int, npc_name: str) -> None:
        """Handles talking to an NPC with improved styling."""
        npc_response = self.city.downtown.talk_to_npc(npc_id, self.main_character)
        self.message_log.append(f"Talked to {npc_name}: {npc_response}")

        # Exibe o diálogo com o NPC
        display_message(self.stdscr, f"{npc_name}: {npc_response}", 2000, curses.color_pair(1))

        # Verifica se o NPC oferece uma missão
        if npc_id == 3 and self.city.downtown.npcs[2].quest is not None:
            self.handle_quest_offer(npc_id, npc_name)


    def handle_quest_offer(self, npc_id: int, npc_name: str) -> None:
        """Handles a quest offer from an NPC with improved styling."""
        self.message_log.append(f"{npc_name} offered a quest.")
        display_message(self.stdscr, f"{npc_name} offered a quest.", 2000, curses.color_pair(1))

        # Exibe as opções de resposta
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
                    self.city.downtown.append_npc_quest(self.main_character, npc_id)
                    self.message_log.append("Quest Accepted")
                    display_message(self.stdscr, "Quest Accepted!", 1500, curses.color_pair(2))
                else:  # Recusar missão
                    self.message_log.append("Quest Denied")
                    display_message(self.stdscr, "Quest Denied.", 1500, curses.color_pair(2))
                break