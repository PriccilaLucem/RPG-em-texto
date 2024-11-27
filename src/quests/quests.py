from typing import Any
from util.id_generator import IDGenerator
class Quests:
    def __init__(self, id:int,  difficult_stars: int, xp_given: int, gold_given: int, mission: str) -> None:
        self.difficult_stars = difficult_stars
        self.xp_given = xp_given
        self.gold_given = gold_given
        self.mission = mission
        self.id= id if id != None else IDGenerator.generate_id()

    def __str__(self) -> str:
        return f"Mission: {self.mission} Difficulty: {self.difficult_stars} stars XP: {self.xp_given} Gold: {self.gold_given}"

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

