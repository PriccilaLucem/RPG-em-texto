from typing import Dict, List
from models.character_model import Character_model
from resources.cave.ores import gold_ore, iron_ore
from enemy.owl_bear.owl_bear import owl_bear, EnemyModel
from models.item_model import ItemsUsedToCraft

class OwlBearCave():
    def __init__(self) -> None:
        self.owl_bear = owl_bear
        self.npcs: List[Character_model] = [
            Character_model("Isman, Brother of Damon", ["Thank you for saving me hero!"]),
            Character_model("Sanael, Brother of Damon", ["We were gathering some ores, and then the creature appeared!"])
        ]
        self.ores = [iron_ore, gold_ore]
        self.has_already_mined = False
        
    def talk_to_npc(self, index: int):
        return self.npcs[index - 1].speech(0)

    @classmethod
    def from_dict(cls, data: Dict) -> None:
        owl_bear_cave = cls()
        owl_bear_cave.owl_bear = EnemyModel.from_dict(data["owl_bear"])
        owl_bear_cave.npcs = [Character_model(npc["name"], npc["speeches"]) for npc in data["npcs"]]
        owl_bear_cave.ores = [ItemsUsedToCraft.from_dict(o) for o in data["ores"]]   
        owl_bear_cave.has_already_mined = data["has_already_mined"]

    def to_dict(self) -> Dict:
        return {
            "owl_bear": self.owl_bear.to_dict(),
            "npcs": [{"name": npc.name, "speeches": npc.speeches} for npc in self.npcs],
            "ores": [o.to_dict() for o in self.ores],
            "has_already_mined": self.has_already_mined
        }
