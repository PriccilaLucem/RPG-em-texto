from models.shop_model import Shop_model
from models.character_model import Character_model
from models.character_with_a_quest_model import Character_with_a_quest_model
from destinations.prismeer.items import generate_armor_from_prismeer_seller, generate_weapon_from_prismeer_seller
from characters.hero import Hero
from typing import List, Union
from quests.quests import Quests

class Comercial_center():
    def __init__(self) -> None:
        self.armor_shop = Shop_model("Two Brothers Armory", "Baron",[
        "Welcome to Two Brothers Armory, what would you like to buy?",
        "We have a great Amory since the foundation of Prissmer",
        "Take a look in my armory, feel at home"], generate_armor_from_prismeer_seller())

        
        self.weapon_shop = Shop_model("Brotherhood of the swords", "Chimaru", [
            "Yo, here we seel swords, only swords. We don't like other weapons",
            "We here opened as a bar, but now we sell swords, because swords are the best",
            "Are you gonna buy or just taking a look?"
        ],generate_weapon_from_prismeer_seller())
        
        self.npcs: List[Union[Character_model, Character_with_a_quest_model]]  = [Character_model("Afrac", [
            "Hello There i'm Afrac, nice to meet you"
        ]), 
        Character_model("Osvaldo",[
            "Do you have any vodka? I want to drink"
        ]),
        Character_with_a_quest_model("Damon", [
        "Hero! Hero! Please you have to help my brothers... They tried to take the treasure of OwBear and now they are trapped in his cave!", 
        "Thank you hero!"
        ],
        Quests(1,2,100,25, "Help the brothes of Damon in OwBear cave!"))
        ]

    def talk_to_npc(self, key:int, main_character:Hero):
        npc_to_talk = self.npcs[key-1]
        if any(quest.id == 1 for quest in main_character.concluded_quests) and key == 3:
            return npc_to_talk.speech(1)
        else:
            return npc_to_talk.speech(0)
                

    def append_npc_quest(self, main_character: Hero):
        main_character.append_quests(self.npcs[2].quest)
        self.npcs[2].quest = None