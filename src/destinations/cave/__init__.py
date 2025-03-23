import curses
from global_state.global_state import should_exit, exit_loop, update_game_state, get_game_state
from util.display_message import draw_menu, display_message, draw_menu_with_history
from util.combat_system import combat
from history.history import the_real_init, entering_owl_bear_cave_first_time, after_owl_bear_battle
from resources import mine
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from characters.main_character import MainCharacter
    from destinations.cave.owl_bear_cave import OwlBearCave
    


class OutsideCave:
    def __init__(self, owl_bear_cave: "OwlBearCave", main_character: "MainCharacter" , stdscr: curses.window, menu):
        self.owl_bear_cave = owl_bear_cave
        self.main_character = main_character
        self.menu = menu
        self.stdscr = stdscr
        self.options = [
            "Menu",
            "Return to Prismeer Surroundings",
            "Enter Cave",
        ]
        self.selected_index = 0
        self.inside_cave = InsideCave(self.owl_bear_cave, self.main_character, self.stdscr, self.menu)

    def run(self):
        """Controla a lógica e interação do jogador fora da caverna."""
        atual_location = get_game_state()["atual_location"]
        if atual_location == "inside_owl_bear_cave":
            self.inside_cave.run()
        if atual_location not in ["inside_owl_bear_cave", "outside_owl_bear_cave"]:
            return
        while not should_exit():
            try:
                self.draw()
                key = self.stdscr.getch()
                self.handle_input(key)
            except StopIteration:
                break
            except Exception as e:
                display_message(self.stdscr, f"An error occurred: {e}", 2000)

    def draw(self):
        """Desenha o menu da entrada da caverna."""
        draw_menu(self.stdscr, "Outside the Cave", self.options, self.selected_index)

    def handle_input(self, key):
        """Processa a entrada do jogador."""
        if key == curses.KEY_UP:
            self.selected_index = max(0, self.selected_index - 1)
        elif key == curses.KEY_DOWN:
            self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
        elif key == ord('\n'):  # Enter key
            self.execute_option()

    def execute_option(self):
        """Executa a ação da opção selecionada."""
        selected_option = self.options[self.selected_index]

        if selected_option == "Enter Cave":
            self.enter_cave()
        elif selected_option == "Menu":
            self.menu.run()
        elif selected_option == "Return to Prismeer Surroundings":
            display_message(self.stdscr, "Returning to previous menu...", 1000, curses.color_pair(1))
            exit_loop("prismeer_surroundings")


    def enter_cave(self):
        """Entra na caverna e inicia a classe InsideCave."""
        update_game_state(cave=self.owl_bear_cave, main_character=self.main_character, atual_location="inside_owl_bear_cave")
        display_message(self.stdscr, "Entering cave...", 1000, curses.color_pair(11))
        self.inside_cave.run()


class InsideCave:
    def __init__(self, owl_bear_cave: "OwlBearCave", main_character: "MainCharacter", stdscr: curses.window, menu):
        self.owl_bear_cave = owl_bear_cave
        self.main_character = main_character
        self.menu = menu
        self.stdscr = stdscr
        self.options = [
            "Talk to First Brother",
            "Talk to Second Brother",
            "Scavenge OwlBear",
            "Mine Resources",
            "Exit Cave"
        ]
        if owl_bear_cave.owl_bear.loot_collected == True:
            self.options.remove("Scavenge OwlBear")
        self.selected_index = 0

    def run(self):
        """Controla a lógica e interação do jogador dentro da caverna."""
        atual_location = get_game_state()["atual_location"]
        if atual_location != "inside_owl_bear_cave":
            return
        update_game_state(cave = self.owl_bear_cave, main_character = self.main_character)
        while not should_exit():
            if not get_game_state().get("combat_done") and any(quest.id == 1 for quest in self.main_character.quests):
                self.handle_combat()
            try:
                self.draw()
                key = self.stdscr.getch()
                self.handle_input(key)
            except StopIteration:
                break
            except Exception as e:
                display_message(self.stdscr, f"An error occurred: {e}", 2000)

    def draw(self):
        """Desenha o menu dentro da caverna."""
        draw_menu(self.stdscr, "Inside the Cave", self.options, self.selected_index)

    def handle_input(self, key):
        """Processa a entrada do jogador."""
        if key == curses.KEY_UP:
            self.selected_index = max(0, self.selected_index - 1)
        elif key == curses.KEY_DOWN:
            self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
        elif key == ord('\n'):  # Enter key
            self.execute_option()

    def execute_option(self):
        """Executa a ação da opção selecionada."""
        selected_option = self.options[self.selected_index]

        if selected_option == "Talk to First Brother":
            display_message(self.stdscr, self.owl_bear_cave.talk_to_npc(1), 1000, curses.color_pair(1))
        elif selected_option == "Talk to Second Brother":
            display_message(self.stdscr, self.owl_bear_cave.talk_to_npc(2), 1000, curses.color_pair(1))
        elif selected_option == "Scavenge OwlBear":
            self.scavenge_owlbear()
        elif selected_option == "Mine Resources":
            self.mine_resources()
        elif selected_option == "Exit Cave":
            self.exit_cave()

    def scavenge_owlbear(self):
        """Coleta itens do Owlbear, se possível."""
        if not self.owl_bear_cave.owl_bear.loot_collected:
            display_message(self.stdscr, self.owl_bear_cave.owl_bear.drop_items(self.main_character), 3000, curses.color_pair(1))
            self.owl_bear_cave.owl_bear.loot_collected = True
            self.options.remove("Scavenge OwlBear")
        else:
            display_message(self.stdscr, "The OwlBear has already been scavenged.", 1000)

    def mine_resources(self):
        """Minerar recursos na caverna."""
        if not self.owl_bear_cave.has_already_mined:
            mine(self.stdscr, self.owl_bear_cave.ores, self.main_character)
            self.owl_bear_cave.has_already_mined = True
            self.options.remove("Mine Resources")
        else:
            display_message(self.stdscr, "You have already mined here.", 1000, curses.color_pair(1))

    def exit_cave(self):
        """Retorna para fora da caverna."""
        display_message(self.stdscr, "Returning to outside the cave...", 1000, curses.color_pair(11))
        exit_loop("outside_owl_bear_cave")

    def handle_combat(self):
        """Lida com o combate contra o Owlbear."""
        cave_history = entering_owl_bear_cave_first_time()
        draw_menu_options = ["Continue"]
        index = 0

        while True:
            draw_menu_with_history(self.stdscr, "===Entering Cave===", cave_history, draw_menu_options, index)
            key = self.stdscr.getch()
            if key == 10:  
                break

        if not combat(self.stdscr, self.main_character, self.owl_bear_cave.owl_bear):
            while True:
                draw_menu_with_history(self.stdscr, "===A vision of hell===", the_real_init(), draw_menu_options, index)
                key = self.stdscr.getch()
                if key == 10:  
                    self.main_character.choose_character_class(self.stdscr)
                    break

        while True:
            draw_menu_with_history(self.stdscr, "===After the battle===", after_owl_bear_battle(), draw_menu_options, index)
            key = self.stdscr.getch()
            if key == 10:  \
                break

        self.main_character.health_points = self.main_character.max_hp
        self.conclude_quest()
        update_game_state(combat_done=True)

    def conclude_quest(self):
        """Conclui a missão relacionada ao combate com o Owlbear."""
        quest_to_remove = next((quest for quest in self.main_character.quests if quest.id == 1), None)
        if quest_to_remove:
            self.main_character.conclude_quests(quest_to_remove)