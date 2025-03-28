from models.quests import Quests, CollectableQuest, DeliverQuestsItems
from typing import Union, TYPE_CHECKING
if TYPE_CHECKING:
    from characters.main_character import MainCharacter
class Character_model:
    def __init__(self, name: str, speeches: list) -> None:
        self.name = name
        self.speeches = speeches    

    def speech(self, list_index: int) -> str:
        try:
            return self.speeches[list_index]
        except IndexError:
            return self.speeches[-1]
    @classmethod
    def from_dict(cls, data: dict) -> None:
        npc = cls(name=data["name"], speeches=data["speeches"])
        return npc
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "speeches": self.speeches
        }

class Character_with_a_quest_model(Character_model):
    def __init__(self, name: str, speeches: list, quest: Union[Quests, CollectableQuest, DeliverQuestsItems ]) -> None:
        super().__init__(name, speeches)
        self.quest = quest 

    @classmethod
    def from_dict(cls, data: dict):
        instance = cls(name=data['name'], speeches=data['speeches'], quest=None)
        quest_data = data.get('quest')
        if quest_data:
            if 'items_to_be_collected' in quest_data:
                instance.quest = CollectableQuest.from_dict(quest_data)
            elif "item_to_be_delivered" in quest_data:
                instance.quest = DeliverQuestsItems.from_dict(quest_data)
            else:
                instance.quest = Quests.from_dict(quest_data)
        else:
            instance.quest = None
        return instance

    def to_dict(self):
        npc = super().to_dict()
        npc['quest'] = self.quest.to_dict() if self.quest else None
        return npc
class Seller_model(Character_model):
    
    def __init__(self, name: str, speeches: list, backpack:list) -> None:
        super().__init__(name, speeches)
        self.backpack = backpack
    
    def show_backpack(self):
        return list(map(str, self.backpack))
        
    
    def sell_item(self, item_id: int, main_character:"MainCharacter") -> None:
            for item in self.backpack:
                if getattr(item, "item_id", None) == item_id:  
                    if MainCharacterold >= getattr(item, "cost", 0):  
                        main_character.backpack.append(item)  
                        self.backpack.remove(item)  
                        MainCharacterold -= getattr(item, "cost", 0)  
                        print(f"You successfully bought {item.name}!")
                        return
                    else:
                        print("You don't have the necessary gold.")
                        return
            print("Item not found in the shop.")
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "speeches": self.speeches,
            "backpack": [item.to_dict() if hasattr(item, "to_dict") else str(item) for item in self.backpack]
        } 

    @classmethod
    def from_dict(cls, data: dict) -> None:
        name = data.get("name")
        speeches = data.get("speeches", [])
        backpack = data.get("backpack", [])
        seller = cls(name=name, speeches=speeches, backpack=backpack)
        return seller   
    
class Bardo(Character_model):
    def __init__(self, name, speeches, price, history):
        self.price = price
        self.history = history
        super().__init__(name, speeches)