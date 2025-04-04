from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from characters.main_character import MainCharacter
import curses
from util.display_message import display_message, draw_menu

class Inn:
    def __init__(self, cost: int, name: str,  stdscr: curses.window) -> None:
        self.cost = cost
        self.name = name
        self.stdscr = stdscr

    def pass_the_night(self, main_character: 'MainCharacter') -> None:
        """Permite ao jogador descansar na pousada."""
        curses.curs_set(0)  # Oculta o cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Texto normal
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Texto de erro
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Títulos e bordas

        selected_index = 0  # Índice da opção selecionada
        options = ["Yes - Rest for the night", "No - Leave the inn"]

        while True:
            # Usa draw_menu para exibir o menu
            draw_menu(self.stdscr, f"Welcome to {self.name}", options, selected_index)

            # Captura a tecla pressionada
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif key == 10:  # Tecla ENTER
                if selected_index == 0:  # Escolheu descansar
                    if main_character.gold < self.cost:
                        display_message(self.stdscr, "You don't have enough gold!", 2000, curses.color_pair(2))
                    else:
                        main_character.gold -= self.cost
                        main_character.hp = main_character.max_hp
                        display_message(self.stdscr, f"You rested at the inn. Remaining gold: {main_character.gold}", 2000, curses.color_pair(1))
                    break
                elif selected_index == 1:  # Escolheu não descansar
                    display_message(self.stdscr, "You chose not to rest.", 2000, curses.color_pair(1))
                    break
            else:  # Escolha inválida
                display_message(self.stdscr, "Invalid choice. Try again.", 1000, curses.color_pair(2))

    @classmethod
    def from_dict(cls, data: Dict, stdscr) -> 'Inn':
        """Cria uma instância de Inn a partir de um dicionário."""
        return cls(cost=data["cost"], name=data["name"], stdscr=stdscr)

    def to_dict(self) -> Dict:
        """Converte a instância de Inn para um dicionário."""
        return {
            "cost": self.cost,
            "name": self.name
        }