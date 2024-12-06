from models.item_model import Sword, LightArmor, HeavyArmor, Axe
from enums.armor_type_enum import Armor_Type_Enum
from enums.rarity_enum import Rarity_Enum
from util.calculate_def_atk import calculate_attack, calculate_defense
def generate_armor_from_prismeer_seller():
    return[
        LightArmor("Leather Vest", calculate_defense(5.0, 1), 5.0, 15, Rarity_Enum.COMMON, Armor_Type_Enum.TORSO),
        HeavyArmor("Iron Chestplate", calculate_defense(10.5, 2), 10.5, 50, Rarity_Enum.UNCOMMON, Armor_Type_Enum.TORSO),
        LightArmor("Rusty Helmet", calculate_defense(5.0, 1), 5.0, 20, Rarity_Enum.COMMON, Armor_Type_Enum.HELMET),
        LightArmor("Traveler's Boots", calculate_defense(3.0, 1), 3.0, 12, Rarity_Enum.COMMON, Armor_Type_Enum.BOOTS),
        HeavyArmor("Steel Helmet", calculate_defense(7.0, 2), 7.0, 30, Rarity_Enum.UNCOMMON, Armor_Type_Enum.HELMET),
        HeavyArmor("Chainmail Pants", calculate_defense(8.5, 2), 8.5, 40, Rarity_Enum.UNCOMMON, Armor_Type_Enum.PANTS),
        HeavyArmor("Reinforced Boots", calculate_defense(6.0, 1), 6.0, 25, Rarity_Enum.COMMON, Armor_Type_Enum.BOOTS),
        HeavyArmor("Knight's Chestplate", calculate_defense(12.5, 3), 12.5, 75, Rarity_Enum.RARE, Armor_Type_Enum.TORSO),
        HeavyArmor("Hardened Leather Pants", calculate_defense(7.5, 1), 7.5, 35, Rarity_Enum.COMMON, Armor_Type_Enum.PANTS),
        HeavyArmor("Golden Helmet", calculate_defense(5.5, 3), 5.5, 100, Rarity_Enum.RARE, Armor_Type_Enum.HELMET),
        LightArmor("Silver Chestplate", calculate_defense(10.0, 2), 10.0, 90, Rarity_Enum.UNCOMMON, Armor_Type_Enum.TORSO),
        HeavyArmor("Plated Boots", calculate_defense(8.0, 2), 8.0, 50, Rarity_Enum.UNCOMMON, Armor_Type_Enum.BOOTS)
    ]
def generate_weapon_from_prismeer_seller():
    return [
        Sword("Steel Longsword", calculate_attack(8.0, 2, 0.2), 8.0, 60, Rarity_Enum.UNCOMMON, 0.2),
        Sword("Golden Blade", calculate_attack(5.0, 3, 0.3), 5.0, 120, Rarity_Enum.RARE, 0.3),
        Sword("Iron Claymore", calculate_attack(12.0, 2, 0.2), 12.0, 75, Rarity_Enum.UNCOMMON, 0.2),
        Sword("Reinforced Broadsword", calculate_attack(6.5, 2, 0.2), 6.5, 50, Rarity_Enum.UNCOMMON, 0.2),
        Sword("Mithril Longsword", calculate_attack(9.0, 3, 0.2), 9.0, 150, Rarity_Enum.RARE, 0.2)
    ]
