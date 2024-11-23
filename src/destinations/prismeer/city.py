from destinations.prismeer.comercial_center import Comercial_center 
from destinations.prismeer.inn import Inn
from quests.quests import Quests
from typing import List

class City():
    
    def __init__(self) -> None:
        self.downtown:Comercial_center = Comercial_center()
        self.billboard: List[Quests] = []
        self.inn:Inn = Inn(20)    
