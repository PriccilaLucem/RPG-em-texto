import curses
import random
from typing import List
from models.item_model import ItemsUsedToCraft
from enums.rarity_enum import Rarity_Enum

def mine(stdscr: curses.window, ores: List[ItemsUsedToCraft], main_character) -> bool:
    rarity_probabilities = {
        Rarity_Enum.COMMON: 1.0,       # 100% chance
        Rarity_Enum.UNCOMMON: 0.5,     # 50% chance
        Rarity_Enum.RARE: 0.2,         # 20% chance
        Rarity_Enum.EPIC: 0.1,         # 10% chance
        Rarity_Enum.LEGENDARY: 0.05    # 5% chance
    }
    mined_ores = []
    max_lines, max_cols = stdscr.getmaxyx()  
    display_line = 0  

    stdscr.clear()
    stdscr.addstr(display_line, 0, "Mining Ores...\n")
    display_line += 1
    stdscr.refresh()

    while len(mined_ores) < 10:
        ore = random.choice(ores)
        if random.random() <= rarity_probabilities.get(ore.rarity, 0):
            mined_ores.append(ore)
          
            if display_line >= max_lines - 1:  
                stdscr.clear()
                display_line = 0
            
            stdscr.addstr(display_line, 0, f"Ore mined: {ore}\n")
            display_line += 1
            stdscr.refresh()

            main_character.add_to_inventory(ore)
            curses.napms(500) 

    if display_line >= max_lines - 1:
        stdscr.clear()
        display_line = 0

    stdscr.addstr(display_line, 0, "\nMining complete! Press any key to return.\n")
    stdscr.refresh()
    stdscr.getch()

    return True
