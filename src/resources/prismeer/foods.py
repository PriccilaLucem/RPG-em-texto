from models.item_model import Food
from enums.rarity_enum import Rarity_Enum

french_fries = Food(name="French Fries", value=15, rarity=Rarity_Enum.COMMON, weight=0.3, health_recovery="15 HP", is_sellable=True)
chiken_wings = Food(name="Chicken Wings", value=25, rarity=Rarity_Enum.UNCOMMON, weight=0.4, health_recovery="25 HP", is_sellable=True)
creaft_burger = Food(name="Craft Burger", value=40, rarity=Rarity_Enum.RARE, weight=0.6, health_recovery="40 HP", is_sellable=True)
beer = Food(name="Beer", value=5, rarity=Rarity_Enum.COMMON, weight=3, health_recovery="10", is_sellable=True)
