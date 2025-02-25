from models.item_model import ItemsUsedToCraft
from enums.rarity_enum import Rarity_Enum

mystical_leaf = ItemsUsedToCraft(name="Mystic Leaf", value=10, rarity=Rarity_Enum.COMMON, weight=0.2),
forest_gem = ItemsUsedToCraft(name="Forest Gem", value=50, rarity=Rarity_Enum.RARE, weight=1.0),
ancient_bark = ItemsUsedToCraft(name="Ancient Bark", value=20, rarity=Rarity_Enum.UNCOMMON, weight=0.5)