from typing import Any, List, Union, Optional, Dict
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
        
        self.equipments: Dict[str, Optional[Union[armor_model.ArmorModel, weapon_model.Weapon_model]]] = {
            "torso": None,
            "helmet": None,
            "pants": None,
            "boots": None,
        }
        
        self.experience:int = 0
        self.next_level_xp:int = 100
        self.attack_points:int = 20
        self.defense_points:int = 20
        self.level:int = 0
        self.critical_hit_chance = 5
        self.resistance_factor = 1
        self.quests: List[Quests] = [Quests(1,2,100,25, "Help the brothes of Damon in OwBear cave!")] 
        self.concluded_quests: List[Quests] = []
        self.speed = 10 


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
    
    def equip_item(self, item: Union[armor_model.ArmorModel, weapon_model.Weapon_model]) -> str:
        if item not in self.backpack:
            return f"Item {item} não está na mochila."
        
        if isinstance(item, weapon_model.Weapon_model):
            self.attack_points += item.attack_points
            self.critical_hit_chance += item.critical_hit_chance
            
            if "weapon" in self.equipments and self.equipments["weapon"] is not None:
                self.backpack.append(self.equipments["weapon"])
            
            self.equipments["weapon"] = item
        
        elif isinstance(item, armor_model.ArmorModel):
            slot = item.type  
            if slot not in self.equipments:
                return f"Slot {slot} inválido para armadura."
            
            self.defense_points += item.defense_points
            self.resistance_factor += item.resistance_factor
            
            if self.equipments[slot] is not None:
                self.backpack.append(self.equipments[slot])
            
            self.equipments[slot] = item
        
        self.backpack.remove(item)
        return f"Item {item} equipado com sucesso!"
