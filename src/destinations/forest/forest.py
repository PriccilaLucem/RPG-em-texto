import random
import curses
from enemy.wolf.wolf import wolf
from enemy.giant_spider.giant_spider import giant_spider
from enemy.treant.treant import treant
from enemy.goblin.goblin import goblin
from resources.forest.crafting_items import all_crafting_items
from resources.forest.rare_items import all_rare_items
from resources.forest.food_items import all_food_items
from characters.hero import Hero
from models.tree_model import regular_forest_tree
from util.combat_system import combat
from typing import Dict

class Forest():
    def __init__(self):
        self.enemies = [wolf, goblin, giant_spider, treant]
        self.resources = all_crafting_items + all_food_items + all_rare_items
        self.trees = 10

    def search_for_resources(self, stdscr: curses.window, main_character: Hero):
        if not self.resources:
            stdscr.addstr("No more resources left in the forest.\n")
            return
        
        chance_to_combat = 0.4

        if chance_to_combat < random.random():
            combat(stdscr, main_character, random.choice(self.enemies))
        
        found_resource = random.choice(self.resources)
        stdscr.addstr(f"You found: {found_resource.name}\n")
        main_character.add_to_inventory(found_resource)

    def take_down_a_tree(self, stdscr: curses.window, main_character: Hero):
        regular_forest_tree.cut_down_a_tree(stdscr, main_character)
        self.trees -= 1
        stdscr.addstr(f"Remaining trees: {self.trees}\n")
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Forest":
        forest = cls()  
        
        enemy_classes = {
            "wolf": wolf,  
            "goblin": goblin,
            "giant_spider": giant_spider,
            "treant": treant
        }
        
        forest.enemies = []
        for enemy_name in data.get("enemies", []):
            if enemy_name in enemy_classes:
                enemy_data = data.get("enemy_data", {}).get(enemy_name, {})
                enemy_class = enemy_classes[enemy_name]
                enemy = enemy_class(**enemy_data)  
                forest.enemies.append(enemy)

        forest.resources = data.get("resources", [])

        forest.trees = data.get("trees", 0)
        
        return forest  
    def to_dict(self) -> Dict:
        return {
            "enemies": [enemy.name for enemy in self.enemies],  
            "resources": [resource.to_dict() for resource in self.resources],  
            "trees": self.trees
        }