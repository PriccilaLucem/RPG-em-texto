from typing import Any, List
from quests.quests import quests

class hero():
    
    def __init__(self) -> None:
        self.hp:int = 50
        self.max_hp:int = 50
        self.gold:int = 0
        self.backpack = []
        
        self.equipments = {
            
        }
        
        self.experience:int = 0
        self.next_level_xp: int= 100
        self.damage:int = 20
        self.level:int = 0
        self.quests: List[quests] = []
        
    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
    
    def level_up(self) -> Any:
        self.level += 1
        self.max_hp += 10
        self.hp += 10
        self.damage = self.damage + self.level + 2
        self.next_level_xp = int(self.next_level_xp * 1.2)
        self.experience = 0
    
    def append_quests(self, quest:quests):
        self.quests.append(quest)
        
    def conclude_quests(self, quest:quests):
        if(quest in self.quests):
            self.gold += quest.gold_given
            if(self.next_level_xp >  self.experience + quest.xp_given):
                self.experience += quest.xp_given
            else:
                xp = quest.xp_given - (self.next_level_xp - self.experience)
                self.level_up()
                self.experience = xp