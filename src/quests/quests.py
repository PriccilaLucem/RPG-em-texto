from typing import Any


class Quests():
    QUESTS_POSSIBILITIES = []
     
    def __init__(self, difficult_stars: int, xp_given: int, gold_given: int, mission: str ) -> None:    
        self.difficult_stars = difficult_stars
        self.xp_given = xp_given
        self.gold_given = gold_given
        self.mission = mission
    
    def __getattribute__(self, name: str) -> Any:
        super().__getattribute__(name)