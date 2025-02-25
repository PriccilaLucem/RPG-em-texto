from models.item_model import ItemsUsedToCraft
from enums.rarity_enum import Rarity_Enum

stick = ItemsUsedToCraft(name="Stick", value=1, rarity=Rarity_Enum.COMMON, weight=0.2)
stone = ItemsUsedToCraft(name="Stone", value=0.5, rarity=Rarity_Enum.COMMON, weight=1.0)
vine = ItemsUsedToCraft(name="Vine", value=1, rarity=Rarity_Enum.UNCOMMON, weight=0.3)
feather = ItemsUsedToCraft(name="Feather", value=2, rarity=Rarity_Enum.RARE, weight=0.05)
tree_resin = ItemsUsedToCraft(name="Tree Resin", value=2.5, rarity=Rarity_Enum.UNCOMMON, weight=0.4)
flint = ItemsUsedToCraft(name="Flint", value=3, rarity=Rarity_Enum.UNCOMMON, weight=0.8)
wood = ItemsUsedToCraft("Wood", 3, Rarity_Enum.COMMON, weight=1.5)


all_crafting_items = [stick, stone, vine, feather, tree_resin, flint]
