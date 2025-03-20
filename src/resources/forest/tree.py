from models.item_model import ItemsUsedToCraft, Food
from enemy.spriggan import spriggan
from enums.rarity_enum import Rarity_Enum
from typing import Dict, Optional

class Tree:
    def __init__(self):
        self.drop = ItemsUsedToCraft(name="Wood", value=1, rarity=Rarity_Enum.COMMON, weight=0.5)  # Default drop
        self.enemy = spriggan  # Default enemy

    # def to_dict(self) -> Dict:
    #     """Convert the Tree instance to a dictionary."""
    #     return {
    #         "drop": self.drop.to_dict() if hasattr(self.drop, 'to_dict') else str(self.drop),
    #         "enemy": self.enemy.to_dict() if hasattr(self.enemy, 'to_dict') else str(self.enemy)
    #     }

    # @classmethod
    # def from_dict(cls, data: Dict) -> "Tree":
    #     """Create a Tree instance from a dictionary."""
    #     tree = cls()
        
    #     # Deserialize the drop
    #     if "drop" in data:
    #         tree.drop = deserialize_resource(data["drop"])
        
    #     # Deserialize the enemy
    #     if "enemy" in data:
    #         tree.enemy = deserialize_enemy(data["enemy"])
        
        # return tree