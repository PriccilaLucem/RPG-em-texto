from enums.rarity_enum import Rarity_Enum
from models.item_model import ItemsUsedToCraft

iron_ore = ItemsUsedToCraft(name="Iron Ore", value=10, rarity=Rarity_Enum.COMMON, weight=2)
gold_ore = ItemsUsedToCraft(name="Gold Ore", value=50, rarity=Rarity_Enum.RARE, weight=1.5)
# silver_ore = ItemsUsedToCraft(name="Silver Ore", value=30, rarity=Rarity_Enum.UNCOMMON, weight=1.8)
# platinum_ore = ItemsUsedToCraft(name="Platinum Ore", value=100,rarity= Rarity_Enum.EPIC, weight=1.2)
# mythril_ore = ItemsUsedToCraft(name="Mythril Ore", value=250,rarity= Rarity_Enum.LEGENDARY, weight=1)
