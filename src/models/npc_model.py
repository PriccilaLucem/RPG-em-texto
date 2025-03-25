from models.quests import Quests, CollectableQuest, DeliverQuestsItems
from typing import Union

class Character_model:
    def __init__(self, name: str, speeches: list) -> None:
        self.name = name
        self.speeches = speeches    

    def speech(self, list_index: int) -> str:
        return self.speeches[list_index]

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
