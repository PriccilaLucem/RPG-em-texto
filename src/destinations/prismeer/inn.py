from typing import Any
from characters.hero import hero

class inn():
    def __init__(self) -> None:
        self.cost = 20
    
    def pass_the_night(self, hero:hero):
        hero.__setattr__("gold", hero.gold - self.cost )
        hero.__setattr__("hp", hero.max_hp)