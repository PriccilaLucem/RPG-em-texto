from models.item_model import Food, ItemsUsedToCraft
from enums.rarity_enum import Rarity_Enum

golden_leaf = ItemsUsedToCraft(name="Golden Leaf", value=50, rarity=Rarity_Enum.LEGENDARY, weight=0.2)
magic_mushroom = Food(name="Magic Mushroom", value=100, rarity=Rarity_Enum.LEGENDARY, weight=0.3, health_recovery=50)
ancient_relic = ItemsUsedToCraft(name="Ancient Relic", value=500, rarity=Rarity_Enum.LEGENDARY, weight=5.0)
spirit_wood = ItemsUsedToCraft(name="Spirit Wood", value=150, rarity=Rarity_Enum.EPIC, weight=2.0)



all_rare_items = [golden_leaf, magic_mushroom, ancient_relic, spirit_wood]
