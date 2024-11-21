from typing import Any


class hero():
    
    def __init__(self) -> None:
        self.hp = 50
        self.max_hp = 50
        self.gold = 0
        self.backpack = []
        self.equipments = []
        self.experience = 0
        self.next_level_xp = 100
        self.damage = 20
        self.level = 0
        
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
            