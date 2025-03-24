from models.horse_model import Horse
from typing import List
from models.npc_model import Character_model

class Stable:
    def __init__(self, horses:List[Horse], owner:Character_model):
        self.horses = horses
        self.owner = owner

    def add_horse(self, horse: Horse):
        self.horses.append(horse)

    def remove_horse(self, horse_name: str):
        self.horses = [horse for horse in self.horses if horse.name != horse_name]

    def list_horses(self):
        return [str(horse) for horse in self.horses]

    def to_dict(self) -> dict:
        return {
            "horses": [horse.to_dict() for horse in self.horses]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Stable":
        instance = cls()
        instance.horses = [Horse.from_dict(h) for h in data.get("horses", [])]
        return instance
