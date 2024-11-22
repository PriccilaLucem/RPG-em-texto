from models.character_model import character_model
from quests.quests import quests

class character_with_a_quest_model(character_model):
    
    def __init__(self, name: str, speeches: list, quest:quests) -> None:
        super().__init__(name, speeches)    
        self.quest:quests = quest