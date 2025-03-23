import curses
from typing import List
from models.quests import Quests, CollectableQuest
from quests import generate_random_quests
from characters.main_character import MainCharacter
from global_state.global_state import exit_loop, should_exit
from util.display_message import display_message, draw_menu

class Billboard:
    def __init__(self, main_character: MainCharacter, stdscr: curses.window) -> None:
        self.quests: List[Quests] = generate_random_quests()
        self.main_character = main_character
        self.stdscr = stdscr

    def billboard_menu(self) -> None:
        selected_index = 0
        options = ["View Available Quests", "Exit Billboard"]
        title = "=== Town Billboard ==="
        
        while True:
            try:
                draw_menu(self.stdscr, title, options, selected_index)
                key = self.stdscr.getch()
                if key == curses.KEY_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif key == curses.KEY_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif key == ord('\n'):  
                    self.handle_options(options[selected_index])
            except StopIteration:
                break
    
    def handle_options(self, option:str):
        if option.startswith("View Available Quests"):
            self.show_quests()
        elif option.startswith("Exit Billboard"):
            exit_loop("prismeer")

    def show_quests(self) -> None:
        if not self.quests:
            display_message(self.stdscr, "No quests available at the moment.", 2000, curses.color_pair(1))
            return

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Título
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Opções normais
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Opção selecionada

        selected_index = 0

        while not should_exit():
            # Cria a lista de opções, incluindo "Exit Billboard Quests"
            quest_options = [str(quest) for quest in self.quests]
            quest_options.append("Exit Billboard Quests")

            # Desenha o menu
            draw_menu(self.stdscr, "=== Available Quests ===", quest_options, selected_index)

            # Captura a tecla pressionada
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(quest_options)  # Move para cima (circular)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(quest_options)  # Move para baixo (circular)
            elif key == 10:  # ENTER
                if selected_index == len(quest_options) - 1:  # Última opção ("Exit Billboard Quests")
                    break  # Sai do loop e retorna ao menu anterior
                else:
                    selected_quest = self.quests[selected_index]
                    display_message(self.stdscr, f"Quest Accepted: {selected_quest}", 1500, curses.color_pair(1))

                    self.main_character.append_quests(self.get_quest_from_billboard(selected_index))
                    self.quests.pop(selected_index)

                    if selected_index >= len(self.quests):
                        selected_index = max(0, len(self.quests) - 1)

                    if not self.quests:
                        display_message(self.stdscr, "No more quests available.", 1500, curses.color_pair(2))
                        break

    def get_quest_from_billboard(self, index: int) -> Quests:
        return self.quests[index]

    @classmethod
    def from_dict(cls, data: dict) -> None:
        billboard = cls()
        billboard.quests = [
            CollectableQuest.from_dict(quest_data) if "items_to_be_collected" in quest_data 
            else Quests.from_dict(quest_data) 
            for quest_data in data["quests"]
        ]
        return billboard
        
    def to_dict(self) -> dict:
        return {"quests": [quest.to_dict() for quest in self.quests]}
