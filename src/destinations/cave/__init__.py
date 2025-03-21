import curses
from global_state.global_state import should_exit, exit_loop, update_game_state, get_game_state
from util.display_message import draw_menu, display_message
from util.combat_system import combat
from history.history import the_real_init
from resources import mine


class OutsideCave:
    def __init__(self, owl_bear_cave, main_character, stdscr, menu):
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
        self.inside_cave = InsideCave(self.owl_bear_cave, self.main_character, self.menu)

    def run(self):
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
            self.return_to_previous_menu()

    def enter_cave(self):
        """Entra na caverna e inicia a classe InsideCave."""
        update_game_state(cave=self.owl_bear_cave, hero=self.main_character, atual_location="cave")
        display_message(self.stdscr, "Entering cave...", 1000)

        # Criar e iniciar a instância da caverna
        self.inside_cave.run(self.stdscr)

    def return_to_previous_menu(self):
        display_message(self.stdscr, "Returning to previous menu...", 1000)
        exit_loop("prismeer_surroundings")


class InsideCave:
    def __init__(self, owl_bear_cave, main_character, menu):
        self.owl_bear_cave = owl_bear_cave
        self.main_character = main_character
        self.menu = menu
        self.options = [
            "Talk to First Brother",
            "Talk to Second Brother",
            "Scavenge Owlbear",
            "Mine Resources",
            "Exit Cave"
        ]
        self.selected_index = 0
        
    def run(self, stdscr):
        """Controla a lógica e interação do jogador dentro da caverna."""
        while not should_exit():
            if not get_game_state().get("combat_done") and any(quest.id == 1 for quest in self.main_character.quests):
                import ipdb
                ipdb.set_trace()
                self.handle_combat(stdscr)
            try:
                self.draw(stdscr)
                key = stdscr.getch()
                self.handle_input(stdscr, key)
            except StopIteration:
                break
            except Exception as e:
                display_message(stdscr, f"An error occurred: {e}", 2000)

    def draw(self, stdscr):
        """Desenha o menu dentro da caverna."""
        draw_menu(stdscr, "Inside the Cave", self.options, self.selected_index)

    def handle_input(self, stdscr, key):
        """Processa a entrada do jogador."""
        if key == curses.KEY_UP:
            self.selected_index = max(0, self.selected_index - 1)
        elif key == curses.KEY_DOWN:
            self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
        elif key == ord('\n'):  # Enter key
            self.execute_option(stdscr)

    def execute_option(self, stdscr):
        """Executa a ação da opção selecionada."""
        selected_option = self.options[self.selected_index]

        if selected_option == "Talk to First Brother":
            display_message(stdscr, self.owl_bear_cave.talk_to_npc(1), 1000)
        elif selected_option == "Talk to Second Brother":
            display_message(stdscr, self.owl_bear_cave.talk_to_npc(2), 1000)
        elif selected_option == "Scavenge Owlbear":
            self.scavenge_owlbear(stdscr)
        elif selected_option == "Mine Resources":
            self.mine_resources(stdscr)
        elif selected_option == "Exit Cave":
            self.exit_cave(stdscr)

    def scavenge_owlbear(self, stdscr):
        """Coleta itens do Owlbear, se possível."""
        if not self.owl_bear_cave.owl_bear.loot_collected:
            display_message(stdscr, self.owl_bear_cave.owl_bear.drop_items(self.main_character), 3000)
        else:
            display_message(stdscr, "The Owlbear has already been scavenged.", 1000)

    def mine_resources(self, stdscr):
        """Minerar recursos na caverna."""
        if not self.owl_bear_cave.has_already_mined:
            mine(stdscr, self.owl_bear_cave.ores, self.main_character)
            self.owl_bear_cave.has_already_mined = True
        else:
            display_message(stdscr, "You have already mined here.", 1000)

    def exit_cave(self, stdscr):
        """Retorna para fora da caverna."""
        display_message(stdscr, "Returning to outside the cave...", 1000)
        exit_loop("cave")

    def handle_combat(self, stdscr):
        """Lida com o combate contra o Owlbear."""
        display_message(stdscr, """
        As you enter the cave, you see two people staring at you, nervously.
        They are looking behind you!
        The OwlBear is angry at you and starts running into your direction!
        """, 3000)

        if not combat(stdscr, self.main_character, self.owl_bear_cave.owl_bear):
            display_message(stdscr, the_real_init(), 3000)
            self.main_character.choose_character_class(stdscr)
            display_message(stdscr, "You wake up to Damon’s brothers frantically trying to wake you up. As you look to the side, you see the lifeless body of the OwlBear...", 5000)

            self.main_character.health_points = self.main_character.max_hp
            self.conclude_quest()

        update_game_state(combat_done=True)

    def conclude_quest(self):
        """Conclui a missão relacionada ao combate com o Owlbear."""
        quest_to_remove = next((quest for quest in self.main_character.quests if quest.id == 1), None)
        if quest_to_remove:
            self.main_character.conclude_quests(quest_to_remove)