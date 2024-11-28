from items.armor_model import ArmorModel
from items.weapon_model import Weapon_model
from enums.armor_type_enum import Armor_Type_Enum
from enums.weapon_type_enum import Weapon_Type_Enum
from enums.rarity_enum import Rarity_Enum

def generate_armor_from_prismeer_seller():
    return [
        ArmorModel("Leather Vest", 2, 5.0, 15,  Rarity_Enum.COMMON, Armor_Type_Enum.TORSO),
        ArmorModel("Iron Chestplate", 5, 10.5, 50 ,Rarity_Enum.UNCOMMON, Armor_Type_Enum.TORSO),
        ArmorModel("Rusty Helmet", 1, 5.0, 20 ,Rarity_Enum.COMMON, Armor_Type_Enum.HELMET),
        ArmorModel("Traveler's Boots", 2, 3.0,12, Rarity_Enum.COMMON, Armor_Type_Enum.BOOTS),
        ArmorModel("Steel Helmet", 3, 7.0, 30, Rarity_Enum.UNCOMMON, Armor_Type_Enum.HELMET),
        ArmorModel("Chainmail Pants", 4, 8.5, 40, Rarity_Enum.UNCOMMON, Armor_Type_Enum.PANTS),
        ArmorModel("Reinforced Boots", 3, 6.0, 25, Rarity_Enum.COMMON, Armor_Type_Enum.BOOTS),
        ArmorModel("Knight's Chestplate", 7, 12.5, 75, Rarity_Enum.RARE, Armor_Type_Enum.TORSO),
        ArmorModel("Hardened Leather Pants", 3, 7.5, 35, Rarity_Enum.COMMON, Armor_Type_Enum.PANTS),
        ArmorModel("Golden Helmet", 6, 5.5, 100, Rarity_Enum.RARE, Armor_Type_Enum.HELMET),
        ArmorModel("Silver Chestplate", 6, 10.0, 90, Rarity_Enum.UNCOMMON, Armor_Type_Enum.TORSO),
        ArmorModel("Plated Boots", 5, 8.0, 50, Rarity_Enum.UNCOMMON, Armor_Type_Enum.BOOTS)
    ]

def generate_weapon_from_prismeer_seller():
    return [
        Weapon_model("Steel Longsword", 8, 8.0, 60, Rarity_Enum.UNCOMMON, Weapon_Type_Enum.SWORD, 0.2),
        Weapon_model("Golden Blade", 12, 5.0, 120, Rarity_Enum.RARE, Weapon_Type_Enum.SWORD, 0.3),
        Weapon_model("Iron Claymore", 10, 12.0, 75, Rarity_Enum.UNCOMMON, Weapon_Type_Enum.LONG_SWORD, 0.2),
        Weapon_model("Reinforced Broadsword", 7, 6.5, 50, Rarity_Enum.UNCOMMON, Weapon_Type_Enum.SWORD, 0.2),
        Weapon_model("Mithril Longsword", 10, 9.0, 95, Rarity_Enum.RARE,Weapon_Type_Enum.SWORD, 0.2)
    ]