from destinations.prismeer.comercial_center import comercial_center 
from destinations.prismeer.inn import inn
from quests import quests

class city():
    
    def __init__(self) -> None:
        self.downtown:comercial_center = comercial_center()
        self.billboard:quests = []
        self.inn = inn()    
