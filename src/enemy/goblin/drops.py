from models.item_model import ItemsUsedToCraft, Dagger

from enums.rarity_enum import Rarity_Enum
goblin_ear = ItemsUsedToCraft(name="Goblin Ear", value=5, rarity=Rarity_Enum.COMMON, weight=0.1)
rusty_dagger = Dagger(name="Rusty Dagger", attack_points=10, weight=0.5, value=30, rarity=Rarity_Enum.COMMON, critical_hit_chance=0.1)


