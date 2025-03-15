from models.character_model import Character_model
from quests.quests import Quests, CollectableQuest
from typing import Union

class Character_with_a_quest_model(Character_model):
    def __init__(self, name: str, speeches: list, quest: Union[Quests, CollectableQuest]) -> None:
        super().__init__(name, speeches)
        self.quest = quest 

    @classmethod
    def from_dict(cls, data: dict):
        instance = cls(name=data['name'], speeches=data['speeches'], quest=None)
        
        quest_data = data.get('quest')
        if quest_data:
            if 'items_to_be_collected' in quest_data:
                instance.quest = CollectableQuest.from_dict(quest_data)
            else:
                instance.quest = Quests.from_dict(quest_data)
        else:
            raise ValueError("'quest' não encontrado nos dados")
        
        return instance

    def to_dict(self):
        npc = super().to_dict()
        npc['quest'] = self.quest.to_dict() if self.quest else None
        return npc
