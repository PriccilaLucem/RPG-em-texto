from models.shop_model import Shop_model
from models.character_model import Character_model
from models.character_with_a_quest_model import Character_with_a_quest_model
from quests.quests import Quests
from items.armor_model import ArmorModel
from items.weapon_model import Weapon_model
from enums.armor_type_enum import Armor_Type_Enum
from enums.rarity_enum import Rarity_Enum
from enums.weapon_type_enum import Weapon_Type_Enum

class Comercial_center():
    def __init__(self) -> None:
        self.armor_shop = Shop_model("Two Brothers Armory", "Baron",[
        "Welcome to Two Brothers Armory, what would you like to buy?",
        "We have a great Amory since the foundation of Prissmer",
        "Take a look in my armory, feel at home"], [
        
        ArmorModel("Leather Vest", 2, 5.0, 15,  Rarity_Enum.COMMON, Armor_Type_Enum.TORSO),
        ArmorModel("Iron Chestplate", 5, 10.5, 50 ,Rarity_Enum.UNCOMMON, Armor_Type_Enum.TORSO),
        ArmorModel("Rusty Helmet", 1, 5.0, 20 ,Rarity_Enum.COMMON, Armor_Type_Enum.HELMET),
        ArmorModel("Traveler’s Boots", 2, 3.0,12, Rarity_Enum.COMMON, Armor_Type_Enum.BOOTS),
        ArmorModel("Steel Helmet", 3, 7.0, 30, Rarity_Enum.UNCOMMON, Armor_Type_Enum.HELMET),
        ArmorModel("Chainmail Pants", 4, 8.5, 40, Rarity_Enum.UNCOMMON, Armor_Type_Enum.PANTS),
        ArmorModel("Reinforced Boots", 3, 6.0, 25, Rarity_Enum.COMMON, Armor_Type_Enum.BOOTS),
        ArmorModel("Knight’s Chestplate", 7, 12.5, 75, Rarity_Enum.RARE, Armor_Type_Enum.TORSO),
        ArmorModel("Hardened Leather Pants", 3, 7.5, 35, Rarity_Enum.COMMON, Armor_Type_Enum.PANTS),
        ArmorModel("Golden Helmet", 6, 5.5, 100, Rarity_Enum.RARE, Armor_Type_Enum.HELMET),
        ArmorModel("Mythril Greaves", 8, 10.0, 150, Rarity_Enum.EPIC, Armor_Type_Enum.BOOTS),
        ArmorModel("Silver Chestplate", 6, 10.0, 90, Rarity_Enum.UNCOMMON, Armor_Type_Enum.TORSO),
        ArmorModel("Dragon Scale Pants", 12, 15.0, 200, Rarity_Enum.LEGENDARY, Armor_Type_Enum.PANTS),
        ArmorModel("Plated Boots", 5, 8.0, 50, Rarity_Enum.UNCOMMON, Armor_Type_Enum.BOOTS)
        
        ])

        
        self.weapon_shop = Shop_model("Brotherhood of the swords", "Chimaru", [
            "Yo, here we seel swords, only swords. We don't like other weapons",
            "We here opened as a bar, but now we sell swords, because swords are the best",
            "Are you gonna buy or just taking a look?"
        ], [
        Weapon_model("Steel Longsword", 8, 8.0, 60, Rarity_Enum.UNCOMMON, Weapon_Type_Enum.SWORD ),
        Weapon_model("Golden Blade", 12, 5.0, 120, Rarity_Enum.RARE, Weapon_Type_Enum.SWORD),
        Weapon_model("Iron Claymore", 10, 12.0, 75, Rarity_Enum.UNCOMMON, Weapon_Type_Enum.LONG_SWORD),
        Weapon_model("Reinforced Broadsword", 7, 6.5, 50, Rarity_Enum.UNCOMMON, Weapon_Type_Enum.SWORD),
        Weapon_model("Mithril Longsword", 10, 9.0, 95, Rarity_Enum.RARE,Weapon_Type_Enum.SWORD )
        ])
        
        self.person1 = Character_model("Afrac", [
            "Hello There i'm Afrac, nice to meet you"
        ])    
        self.person2 = Character_model("Osvaldo",[
            "Do you have any vodka? I want to drink"
        ])
        self.person3 = Character_with_a_quest_model("Damon", [
        "Hero! Hero! Please you have to help my brothers... They tried to take the treasure of OwBear and now they are trapped in his cave!", 
        "Thank you hero!"
        ],
        quest=Quests(2,100,50, "Help the brothes of Damon in OwBear cave!")
                                            
        )

    