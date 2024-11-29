from enemy.owl_bear import OwlBear  
from typing import List
from models.character_model import Character_model
class OwlBearCave():
    def __init__(self) -> None:
        self.owl_bear = OwlBear()
        self.npcs: List[Character_model] = [Character_model("Isman, Brother of Damon", ["Thank you for saving me hero!"]),
                                   Character_model("Sanael, Brother of Damon",["We were gathering some ores, and then the creature appeared!"])]
        # self.ores = []

    def talk_to_npc(self, index ):
        return self.npcs[index -1].speech(0)