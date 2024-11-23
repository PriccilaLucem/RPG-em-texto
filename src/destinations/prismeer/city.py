from destinations.prismeer.comercial_center import comercial_center 
from destinations.prismeer.inn import Inn
from quests.quests import quests
from typing import List

class city():
    
    def __init__(self) -> None:
        self.downtown:comercial_center = comercial_center()
        self.billboard: List[quests] = []
        self.inn:Inn = Inn(20)    
