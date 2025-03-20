from enums.rarity_enum import Rarity_Enum
from typing import Optional, Dict
from models.item_model import Food, ItemsUsedToCraft

def deserialize_resource(data: Dict) -> Optional[ItemsUsedToCraft]:
    """Convert a dictionary into a resource object."""
    if not isinstance(data, dict):
        return None
    
    if "health_recovery" in data:
        # Deserialize as Food
        return Food(
            name=data.get("name", "Unknown Food"),
            value=data.get("value", 0),
            rarity=Rarity_Enum[data.get("rarity", Rarity_Enum.COMMON.name)],
            weight=data.get("weight", 0),
            health_recovery=data.get("health_recovery", 0)
        )
    else:
        # Deserialize as ItemsUsedToCraft
        return ItemsUsedToCraft(
            name=data.get("name", "Unknown Item"),
            value=data.get("value", 0),
            rarity=Rarity_Enum[data.get("rarity", Rarity_Enum.COMMON.name)],
            weight=data.get("weight", 0)
        )