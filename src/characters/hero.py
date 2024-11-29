from typing import Any, List, Union, Optional, Dict
from quests.quests import Quests
from items import armor_model, weapon_model
from enums import weapon_type_enum, rarity_enum
from models.abilities_model import Ability_Model
import curses
class Hero():
    
    def __init__(self) -> None:
        self.name: str = "Hero" 
        self.health_points:int = 50
        self.max_hp:int = 50
        self.gold:int = 1000000
        self.backpack:List[Union[armor_model.ArmorModel, weapon_model.Weapon_model]] = [
        weapon_model.Weapon_model("Wooden sword", 2, 0.5, 5, rarity_enum.Rarity_Enum.COMMON, weapon_type_enum.Weapon_Type_Enum.SWORD, 0.1)
        ]
        self.abilities: List[Ability_Model] = []
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
        self.attack_multiplier = 1

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
    
    def level_up(self) -> Any:
        self.level += 1
        self.max_hp += 10
        self.health_points += 10
        self.defense_points += 0.5
        self.attack_points += 0.5
        self.speed = self.speed * 1.1
        self.attack_points = self.attack_points + self.level + 2
        self.next_level_xp = int(self.next_level_xp * 1.2)
        self.experience = 0
    
    def append_quests(self, quest:Quests):
        self.quests.append(quest)
        
    def init_a_quest(self, quest:Quests):
        self.quests.append(quest)
    
    def conclude_quests(self, quest: Quests):
        # Verifica se a quest é válida e está na lista
        if not quest:
            raise ValueError("Quest cannot be None.")
        if quest not in self.quests:
            raise ValueError("Quest is not part of the active quests list.")
    
        # Adiciona o ouro da quest
        self.gold += quest.gold_given
    
        # Adiciona experiência e verifica se há necessidade de subir de nível
        if self.experience + quest.xp_given < self.next_level_xp:
            self.experience += quest.xp_given
        else:
            # Calcula o XP remanescente após o level up
            remaining_xp = (self.experience + quest.xp_given) - self.next_level_xp
            self.level_up()
            self.experience = remaining_xp
    
    def equip_item(self, item: Union[armor_model.ArmorModel, weapon_model.Weapon_model]) -> str:
        if item not in self.backpack:
            return f"Item {item} não está na mochila."
        
        if isinstance(item, weapon_model.Weapon_model):
            self.attack_points += item.attack_points
            self.critical_hit_chance += item.critical_hit_chance
            
            if "weapon" in self.equipments and self.equipments["weapon"] is not None:
                self.backpack.append(self.equipments["weapon"])
            
            self.equipments["weapon"] = item
            self.critical_hit_chance += item.critical_hit_chance
        elif isinstance(item, armor_model.ArmorModel):
            slot = item.type
            if slot not in self.equipments:
                return f"Slot {slot} inválido para armadura."
            
            self.defense_points += item.def_points
            
            if self.equipments[slot] is not None:
                self.backpack.append(self.equipments[slot])
            
            self.equipments[slot] = item
        
        self.backpack.remove(item)
        return f"Item {item} equipado com sucesso!"
    
    def show_inventory(self, stdscr: curses.window):
        current_row = 0
        
        while True:
            stdscr.clear()
            stdscr.addstr("Use ↑ and ↓ to navigate, Enter to select an item, and 'q' to quit.\n\n")
            
            for idx, item in enumerate(self.backpack):
                if idx == current_row:
                    stdscr.addstr(f"> {item}\n", curses.A_REVERSE)
                else:
                    stdscr.addstr(f"  {item}\n")
            
            key = stdscr.getch()
            
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.backpack) - 1:
                current_row += 1
            elif key == ord('\n'):  # Enter key
                selected_item = self.backpack[current_row]
                result = self.equip_item(selected_item)
                stdscr.clear()
                stdscr.addstr(result + "\n")
                stdscr.addstr("Press any key to continue...")
                stdscr.getch()
            elif key == ord('q'):  # Quit
                break
            
            stdscr.refresh()