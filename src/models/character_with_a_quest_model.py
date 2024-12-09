from models.character_model import Character_model
from quests.quests import Quests, CollectableQuest
from typing import Union

class Character_with_a_quest_model(Character_model):
    
    def __init__(self, name: str, speeches: list, quest:Quests) -> None:
        super().__init__(name, speeches)    
        self.quest:Union[Quests, CollectableQuest] = quest