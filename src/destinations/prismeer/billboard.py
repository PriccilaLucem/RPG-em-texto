import curses
from typing import List
from models.quests import Quests, CollectableQuest
from quests import generate_random_quests
from characters.main_character import MainCharacter
from global_state.global_state import exit_loop, should_exit
from util.display_message import display_message, draw_menu

class Billboard:
    def __init__(self, stdscr: curses.window) -> None:
        self.quests: List[Quests] = generate_random_quests()
        self.stdscr = stdscr

    def billboard_menu(self, main_character: MainCharacter) -> None:
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
                    if  options[selected_index].startswith("View Available Quests"):
                        self.show_quests(main_character)
                    elif options[selected_index].startswith("Exit Billboard"):
                       exit_loop("prismeer")
            except StopIteration:
                break
    
    def show_quests(self, main_character: MainCharacter) -> None:
        if not self.quests:
            display_message(self.stdscr, "No quests available at the moment.", 2000, curses.color_pair(1))
            return

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Título
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Opções normais
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Opção selecionada

        selected_index = 0

        while True:
            quest_options = [str(quest) for quest in self.quests]
            quest_options.append("Exit Billboard Quests")

            draw_menu(self.stdscr, "=== Available Quests ===", quest_options, selected_index)

            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(quest_options)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(quest_options)
            elif key == 10:  
                if selected_index == len(quest_options) - 1:  
                    break
                else:
                    selected_quest = self.quests[selected_index]
                    display_message(self.stdscr, f"Quest Accepted: {selected_quest}", 1500, curses.color_pair(1))

                    main_character.append_quests(self.get_quest_from_billboard(selected_index))
                    self.quests.pop(selected_index)

                    if selected_index >= len(self.quests):
                        selected_index = max(0, len(self.quests) - 1)

                    if not self.quests:
                        display_message(self.stdscr, "No more quests available.", 1500, curses.color_pair(2))
                        break

    def get_quest_from_billboard(self, index: int) -> Quests:
        return self.quests[index]

    @classmethod
    def from_dict(cls, data: dict, stdsc) -> None:
        billboard = cls(stdsc)
        billboard.quests = [
            CollectableQuest.from_dict(quest_data) if "items_to_be_collected" in quest_data 
            else Quests.from_dict(quest_data) 
            for quest_data in data["quests"]
        ]
        return billboard
        
    def to_dict(self) -> dict:
        return {"quests": [quest.to_dict() for quest in self.quests]}
