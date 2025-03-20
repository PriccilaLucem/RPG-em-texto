import curses
from typing import List
from quests.quests import Quests, CollectableQuest
from quests import generate_random_quests
from characters.hero import Hero
from global_state.global_state import set_exit, should_exit
from util.display_message import display_message, draw_menu

class Billboard:
    def __init__(self) -> None:
        self.quests: List[Quests] = generate_random_quests()

    def billboard_menu(self, stdscr: curses.window, main_character: Hero) -> None:
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Título
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Texto normal
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Seleção
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)   # Item selecionado

        selected_index = 0
        options = ["View Available Quests", "Exit Billboard"]

        while not should_exit():
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # Desenha a borda
            stdscr.border()

            # Título centralizado
            title = "=== Town Billboard ==="
            stdscr.addstr(2, (width - len(title)) // 2, title, curses.color_pair(1))

            # Instruções centralizadas
            instructions = "Use ↑/↓ to navigate, ENTER to select, ESC to exit."
            stdscr.addstr(4, (width - len(instructions)) // 2, instructions, curses.color_pair(2))

            # Desenha as opções do menu
            for idx, option in enumerate(options):
                x = (width - len(option)) // 2
                y = 6 + idx
                if idx == selected_index:
                    stdscr.addstr(y, x, f"> {option} <", curses.color_pair(4))
                else:
                    stdscr.addstr(y, x, f"  {option}  ", curses.color_pair(2))

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif key == 10:  # Tecla ENTER
                if selected_index == 0:
                    self.show_quests(stdscr, main_character)
                else:
                    break
            elif key == 27:  # Tecla ESC
                set_exit()
                break

    def show_quests(self, stdscr: curses.window, main_character: Hero) -> None:
        if not self.quests:
            display_message(stdscr, "No quests available at the moment.", 2000, curses.color_pair(2))
            return

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Seleção
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Texto normal
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Título

        selected_index = 0

        while not should_exit():
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # Desenha a borda
            stdscr.border()

            # Título centralizado
            title = "=== Available Quests ==="
            stdscr.addstr(2, (width - len(title)) // 2, title, curses.color_pair(3) | curses.A_BOLD)

            # Desenha as missões disponíveis
            for idx, quest in enumerate(self.quests):
                x = (width - len(str(quest))) // 2
                y = 4 + idx
                if idx == selected_index:
                    stdscr.addstr(y, x, f"> {quest} <", curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, f"  {quest}  ", curses.color_pair(2))

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP and selected_index > 0:
                selected_index -= 1
            elif key == curses.KEY_DOWN and selected_index < len(self.quests) - 1:
                selected_index += 1
            elif key == 10:  # ENTER
                selected_quest = self.quests[selected_index]
                stdscr.clear()
                stdscr.border()
                stdscr.addstr(2, (width - len("Quest Accepted!")) // 2, "Quest Accepted!", curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(4, (width - len(f"{selected_quest}")) // 2, f"{selected_quest}", curses.color_pair(2))
                stdscr.refresh()
                main_character.append_quests(self.get_quest_from_billboard(selected_index))
                self.quests.pop(selected_index)
                curses.napms(1500)
                break
            elif key == 27:  # ESC
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
