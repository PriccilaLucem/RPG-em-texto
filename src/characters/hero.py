from typing import Any, List, Union
from quests.quests import Quests
from items import armor_model, weapon_model
from enums import weapon_type_enum, rarity_enum
class Hero():
    
    def __init__(self) -> None:
        self.hp:int = 50
        self.max_hp:int = 50
        self.gold:int = 1000000
        self.backpack:List[Union[armor_model.ArmorModel, weapon_model.Weapon_model]] = [
        weapon_model.Weapon_model("Wooden sword", 2, 0.5, 5, rarity_enum.Rarity_Enum.COMMON, weapon_type_enum.Weapon_Type_Enum.SWORD)
        ]
        
        self.equipments = {
            "torso": "",
            "helmet": "",
            "pants": "",  
        }
        
        self.experience:int = 0
        self.next_level_xp:int = 100
        self.damage:int = 20
        self.level:int = 0
        self.quests: List[Quests] = [] 
        
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
    
    def append_quests(self, quest:Quests):
        self.quests.append(quest)
        
    def init_a_quest(self, quest:Quests):
        self.quests.append(quest)
    
    def show_backpack(self):
        return "\n".join(map(str, self.backpack))  
    
    def conclude_quests(self, quest:Quests):
        if(quest in self.quests):
            self.gold += quest.gold_given
            if(self.next_level_xp >  self.experience + quest.xp_given):
                self.experience += quest.xp_given
            else:
                xp = quest.xp_given - (self.next_level_xp - self.experience)
                self.level_up()
                self.experience = xp
    
    def show_active_quests(self):
        return "\n".join(str(quest) for quest in self.quests)
    
    