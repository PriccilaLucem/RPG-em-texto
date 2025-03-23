import curses
import random
from typing import List
from models.item_model import ItemsUsedToCraft
from enums.rarity_enum import Rarity_Enum
from util.display_message import display_message, display_message_log


def mine(stdscr: curses.window, ores: List[ItemsUsedToCraft], main_character) -> bool:
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    rarity_probabilities = {
        Rarity_Enum.COMMON: 1.0,
        Rarity_Enum.UNCOMMON: 0.5,
        Rarity_Enum.RARE: 0.2,
        Rarity_Enum.EPIC: 0.1,
        Rarity_Enum.LEGENDARY: 0.05
    }

    mined_ores = []
    message_log = []

    # Limpa a tela e desenha a borda inicial
    stdscr.clear()
    stdscr.attron(curses.color_pair(2))
    stdscr.border()
    stdscr.attroff(curses.color_pair(2))
    stdscr.refresh()

    display_message(stdscr, "=== Mining Ores ===", 500, curses.color_pair(2) | curses.A_BOLD)

    while len(mined_ores) < 10:
        ore = random.choice(ores)
        if random.random() <= rarity_probabilities.get(ore.rarity, 0):
            mined_ores.append(ore)

            if ore.rarity == Rarity_Enum.COMMON:
                color = curses.color_pair(1)
            elif ore.rarity == Rarity_Enum.UNCOMMON:
                color = curses.color_pair(2)
            elif ore.rarity == Rarity_Enum.RARE:
                color = curses.color_pair(3)
            elif ore.rarity == Rarity_Enum.EPIC:
                color = curses.color_pair(4) | curses.A_BOLD
            elif ore.rarity == Rarity_Enum.LEGENDARY:
                color = curses.color_pair(5) | curses.A_BOLD
            else:
                color = curses.color_pair(1)

            message = f"Ore mined: {ore.name} ({ore.rarity.name})"
            message_log.append((message, color))
            display_message_log(stdscr, message_log)

            main_character.add_to_inventory(ore)
            curses.napms(500)
    
    # Redesenha a borda antes de exibir a mensagem final
    display_message(stdscr, "Mining complete! Press any key to return.", 1000, curses.color_pair(2) | curses.A_BOLD)
    stdscr.getch()

    return True
