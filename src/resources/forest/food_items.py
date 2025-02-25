from models.item_model import Food
from enums.rarity_enum import Rarity_Enum

red_berry = Food(name="Red Berry", value=0.5, rarity=Rarity_Enum.COMMON, weight=0.1, health_recovery=5)
blue_berry = Food(name="Blue Berry", value=0.5, rarity=Rarity_Enum.COMMON, weight=0.1, health_recovery=7)
apple = Food(name="Apple", value=1, rarity=Rarity_Enum.COMMON, weight=0.2, health_recovery=10)
mushroom = Food(name="Mushroom", value=1.5, rarity=Rarity_Enum.UNCOMMON, weight=0.1, health_recovery=15)
wild_honey = Food(name="Wild Honey", value=3, rarity=Rarity_Enum.RARE, weight=0.5, health_recovery=20)

all_food_items = [red_berry, blue_berry, apple, mushroom, wild_honey]