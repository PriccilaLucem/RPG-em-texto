# import random
# import curses
# from typing import List
# from enemy.wolf.wolf import wolf
# from enemy.giant_spider.giant_spider import giant_spider
# from enemy.treant.treant import treant
# from enemy.goblin.goblin import goblin
# from resources.forest.crafting_items import all_crafting_items
# from resources.forest.rare_items import all_rare_items
# from resources.forest.food_items import all_food_items
# from characters.MainCharacter import MainCharacter
# from models.tree_model import regular_forest_tree
# from util.combat_system import combat
# from typing import Dict
# from models.enemy_model import EnemyModel

# import random
# import curses
# from typing import List, Dict
# from characters.MainCharacter import MainCharacter
# from models.tree_model import regular_forest_tree
# from util.combat_system import combat
# from models.enemy_model import EnemyModel
# from util.deserialize_resource import deserialize_resource

# class Forest:
#     def __init__(self):
#         self.enemies: List[EnemyModel] = [wolf, goblin, giant_spider, treant]
#         self.resources = all_crafting_items + all_food_items + all_rare_items
#         self.trees = 10

#     def search_for_resources(self, stdscr: curses.window, MainCharacter: MainCharacter):
#         if not self.resources:
#             stdscr.addstr("No more resources left in the forest.\n")
#             return
        
#         chance_to_combat = 0.4

#         if random.random() < chance_to_combat:
#             combat(stdscr, MainCharacter, random.choice(self.enemies))
        
#         found_resource = random.choice(self.resources)
#         stdscr.addstr(f"You found: {found_resource.name}\n")
#         MainCharacter.add_to_inventory(found_resource)
#         self.resources.remove(found_resource)  # Remove the resource from the forest

#     def take_down_a_tree(self, stdscr: curses.window, MainCharacter: MainCharacter):
#         if self.trees <= 0:
#             stdscr.addstr("No more trees left in the forest.\n")
#             return
        
#         regular_forest_tree.cut_down_a_tree(stdscr, MainCharacter)
#         self.trees -= 1
#         stdscr.addstr(f"Remaining trees: {self.trees}\n")

#     def to_dict(self) -> Dict:
#         return {
#             "enemies": [enemy.name for enemy in self.enemies],  
#             "resources": [resource.to_dict() if hasattr(resource, 'to_dict') else str(resource) for resource in self.resources],  
#             "trees": self.trees
#         }
    
#     @classmethod
#     def from_dict(cls, data: Dict) -> "Forest":
#         forest = cls()  
        
#         enemy_classes = {
#             "wolf": wolf,  
#             "goblin": goblin,
#             "giant_spider": giant_spider,
#             "treant": treant
#         }
        
#         forest.enemies = []
#         for enemy_name in data.get("enemies", []):
#             if enemy_name in enemy_classes:
#                 enemy_data = data.get("enemy_data", {}).get(enemy_name, {})
#                 enemy_class = enemy_classes[enemy_name]
#                 try:
#                     enemy = enemy_class(**enemy_data)  
#                     forest.enemies.append(enemy)
#                 except TypeError as e:
#                     print(f"Error initializing {enemy_name}: {e}")
#                     continue  # Skip this enemy if initialization fails

#         # Deserialize resources if they are dictionaries
#         forest.resources = []
#         for resource_data in data.get("resources", []):
#             if isinstance(resource_data, dict):
#                 # Assuming you have a function or class to deserialize resources
#                 resource = deserialize_resource(resource_data)  # Replace with actual deserialization logic
#                 forest.resources.append(resource)
#             else:
#                 forest.resources.append(resource_data)

#         forest.trees = data.get("trees", 0)
        
#         return forest  

#     def to_dict(self) -> Dict:
#         return {
#             "enemies": [enemy.name for enemy in self.enemies],  
#             "resources": [resource.to_dict() if hasattr(resource, 'to_dict') else str(resource) for resource in self.resources],  
#             "trees": self.trees
#         }