from models.shop_model import Shop_model
from models.character_model import Character_model
from models.character_with_a_quest_model import Character_with_a_quest_model
from quests.quests import Quests

class Comercial_center():
    def __init__(self) -> None:
        self.armor_shop = Shop_model("Two Brothers Armory", "Baron",[
        "Welcome to Two Brothers Armory, what would you like to buy?",
        "We have a great Amory since the foundation of Prissmer",
        "Take a look in my armory, feel at home"], [])
        
        self.weapon_shop = Shop_model("Brotherhood of the swords", "Chimaru", [
            "Yo, here we seel swords, only swords. We don't like other weapons",
            "We here opened as a bar, but now we sell swords, because swords are the best",
            "Are you gonna buy or just taking a look?"
        ], [])
        
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

    