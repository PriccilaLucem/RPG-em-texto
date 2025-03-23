from resources.forest.crafting_items import wood
from enemy.spriggan.spriggan import spriggan
import curses
from characters.main_character import MainCharacter
from typing import List, Union
from models.item_model import ItemsUsedToCraft, Food  
from models.enemy_model import EnemyModel
import random
from util.combat_system import combat

class Tree():
    def __init__(self, drops: List[Union[ItemsUsedToCraft, Food]], enemies: List[EnemyModel]):
        self.drops = drops
        self.enemies = enemies

    def cut_down_a_tree(self, stdscr: curses.window, MainCharacter: MainCharacter):
        stdscr.addstr("You cut down the tree and collect the drops.\n")
        for drop in self.drops:
            stdscr.addstr(f"Collected: {drop.name}\n")
            MainCharacter.add_to_inventory(drop)
        if self.appear_enemy():
            enemy = random.choice(self.enemies)
            stdscr.addstr(f"A wild {enemy.name} appears!\n")
            combat(stdscr, MainCharacter, enemy)
            
    def appear_enemy(self) -> bool:
        return random.random() < 0.3


regular_forest_tree = Tree([wood], [spriggan])