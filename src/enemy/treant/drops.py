from models.item_model import ItemsUsedToCraft
from enums.rarity_enum import Rarity_Enum

ancient_bark = ItemsUsedToCraft(
    name="Ancient Bark",
    value=50,
    rarity=Rarity_Enum.RARE,
    weight=2.0
)

glowing_sap = ItemsUsedToCraft(
    name="Glowing Sap",
    value=40,
    rarity=Rarity_Enum.UNCOMMON,
    weight=0.5
)