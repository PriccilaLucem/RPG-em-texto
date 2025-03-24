import curses
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from characters.main_character import MainCharacter
    from destinations.nitna_village.nitna import Nitna
    from menu.menu import Menu
    from models.horse_model import Horse
from global_state.global_state import  exit_loop, update_game_state, get_game_state
from util.display_message import display_message, draw_menu, draw_menu_with_history
from history.history import init_of_the_history

class NitnaVillage:
    def __init__(self, nitna: "Nitna", stdscr: curses.window, main_character: "MainCharacter", menu: "Menu"):
        self.stdscr = stdscr
        self.main_character = main_character
        self.nitna = nitna
        self.menu = menu
        self.options = [
            "Menu",
            "Go to Crossroads",
            "Talk to Larid",
            "Talk to Monael",
            "See the Stable"
        ]
        self.selected_index = 0

    def run(self):   
        game_state = get_game_state()

        if game_state.get("atual_location") != "nitna_village":
            return
        if game_state.get("is_new_game"):
            self.history()
        
        while True:   
            try:
                update_game_state(main_character = self.main_character, nitna = self.nitna)
                self.draw()
                key = self.stdscr.getch()
                self.handle_input(key)
            except Exception as e:
                display_message(self.stdscr, f"An error occurred: {e}", 2000)

    def draw(self):
        """Desenha o menu de Nitna Village."""
        draw_menu(self.stdscr, "Nitna Village", self.options, self.selected_index)

    def handle_input(self, key):
        """Processa a entrada do jogador."""
        if key == curses.KEY_UP:
            self.selected_index = max(0, self.selected_index - 1)
        elif key == curses.KEY_DOWN:
            self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
        elif key == ord('\n'):  
            self.execute_option()

    def history(self):
        
        index = 0
        title = "=== AFTER A HORRIBLE NIGHTMARE ==="
        options = ["Continue"]
        while True:
            draw_menu_with_history(self.stdscr, title, init_of_the_history(), options, index)
            key = self.stdscr.getch()
            if key == 10:
                display_message(self.stdscr, self.nitna.mother.speech(0), 2000, curses.color_pair(1))
                display_message(self.stdscr, "Go to prismeer to deliever the sword", 1000, curses.color_pair(1))
                self.main_character.append_quests(self.nitna.mother.quest)
                self.nitna.mother.quest = None
                break

    def execute_option(self):
        """Executa a ação da opção selecionada."""
        selected_option = self.options[self.selected_index]

        if selected_option == "Menu":
            self.menu.run()
        elif selected_option == "Go to Crossroads":
            display_message(self.stdscr, "Going to Crossroads...", 1000, curses.color_pair(1))
            exit_loop("crossroads")
        elif selected_option == "Talk to Larid":
            self.nitna.talk_to_npc("Larid")
        elif selected_option == "Talk to Monael":
            self.nitna.talk_to_npc("Monael")
        elif selected_option == "See the Stable":
            self.view_stable()    

    def view_stable(self):
        options = [
            "See the horses",
            "Talk to Nitz",
            "Exit",
        ]
        index = 0
        title = "=== HORNET STABLE ==="
        while True:
            draw_menu(self.stdscr, title, options, index)
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                index = max(0, index - 1)
            elif key == curses.KEY_DOWN:
                index = min(len(options) - 1, index + 1)
            elif key == 10:  
                if options[index].startswith("See the horses"):
                    self.display_horses()
                elif options[index].startswith("Talk to Nitz"):
                    self.talk_to_nitz()
                else:
                    break
                                
    def display_horses(self):
        options = [horse.__str__() for horse in self.nitna.stable.horses] + ["Exit"]
        index = 0
        title = "=== AVAILABLE HORSES ==="
        options = [str(horse) for horse in self.nitna.stable.horses] + ["Exit"]
        index = 0
            
        while True:
            draw_menu(self.stdscr, title, options, index)
            key = self.stdscr.getch()
                
            if key == curses.KEY_UP:
                index = max(0, index - 1)
            elif key == curses.KEY_DOWN:
                index = min(len(options) - 1, index + 1)
            elif key == 10:
                if index == options[index].startswith("Exit"):  
                    break
                else:
                    self.sell_horse(self.nitna.stable.horses[index])

    def sell_horse(self, horse: "Horse"):
        """Handle horse purchase using custom message display"""
        if self.main_character.gold >= horse.price:
            message = f"Buy {horse.name} for {horse.price} gold?\n\n[Y] Yes  [N] No"
            options = ["Yes", "No"]
            
            while True:
                draw_menu(self.stdscr, "CONFIRM PURCHASE", options,  0, message)
                key = self.stdscr.getch()
                if key in [ord('y'), ord('Y')]:
                    self.main_character.gold -= horse.price
                    self.nitna.stable.horses.remove(horse)
                    self.stdscr.getch()
                    return
                elif key in [ord('n'), ord('N'), 27]:  # ESC or N
                    return
        else: 
            display_message(self.stdscr, "You have no money!", 1000, curses.color_pair(1))
    def talk_to_nitz(self):
        """Handle conversation with Nitz using custom display"""
        dialogue_index = 0 if not hasattr(self, '_last_dialogue') else 1 - self._last_dialogue
        self._last_dialogue = dialogue_index
        
        message = f"Nitz: \"{self.nitna.stable.owner.speeches[dialogue_index]}\""
        display_message(self.stdscr, message, 2000, curses.color_pair(1))