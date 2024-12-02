from typing import Any, List, Union, Optional, Dict
from quests.quests import Quests
from models.item_model import ArmorModel, WeaponModel
from models.abilities_model import BaseAbility
from models.character_class_model import CharacterClass
from classes.cleric import Cleric
from classes.paladin import Paladin
from classes.rogue import Rogue
from classes.paladin import Paladin
from classes.wizard import Wizard
from classes.warrior import Warrior

import curses
class Hero():
    
    def __init__(self) -> None:
        self.name: str = "Hero" 
        self.health_points:int = 50
        self.max_hp:int = 50
        self.gold:int = 1000000
        self.backpack:List[Union[WeaponModel, ArmorModel]] = []
        self.abilities: List[BaseAbility] = []
        self.equipments: Dict[str, Optional[Union[ArmorModel, WeaponModel]]] = {
            "torso": None,
            "helmet": None,
            "pants": None,
            "boots": None,
            "weapons": None
        }
        self.character_class:CharacterClass = None 
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
        self.proficiencies = []
        self.extra_actions = 0
        self.dodge_chance = 0
        self.health = 100
        self.last_attack_damage = 0
        self.carry_weight = 10
        self.weight = 0
    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
    
    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.health_points += 10
        self.defense_points += 0.5
        self.attack_points += 0.5
        self.speed *= 1.1
        self.attack_points += self.level + 2
        self.next_level_xp = int(self.next_level_xp * 1.2)
        self.experience = 0
    
        if self.character_class:
            if self.character_class.name == "Fighter":
                self.attack_points += 3
                self.defense_points += 2
                self.health_points += 5
                self.carry_weight += 2
            elif self.character_class.name == "Rogue":
                self.attack_points += 2
                self.critical_hit_chance += 2
                self.speed += 2
                self.carry_weight += 1
            elif self.character_class.name == "Wizard":
                self.resistance_factor += 0.1
            elif self.character_class.name == "Cleric":
                self.defense_points += 1
                self.health_points += 5
                self.carry_weight += 3
            elif self.character_class.name == "Paladin":
                self.attack_points += 2
                self.defense_points += 2
                self.resistance_factor += 0.05
                self.carry_weight += 4
    
    def append_quests(self, quest:Quests):
        self.quests.append(quest)
        
    def init_a_quest(self, quest:Quests):
        self.quests.append(quest)
    
    def conclude_quests(self, quest: Quests):
        if not quest:
            raise ValueError("Quest cannot be None.")
        if quest not in self.quests:
            raise ValueError("Quest is not part of the active quests list.")

        self.gold += quest.gold_given

        if self.experience + quest.xp_given < self.next_level_xp:
            self.experience += quest.xp_given
        else:
            remaining_xp = (self.experience + quest.xp_given) - self.next_level_xp
            self.level_up()
            self.experience = remaining_xp
    
    def equip_item(self, item: Union[ArmorModel, WeaponModel]) -> str:
        if item not in self.backpack:
            return f"Item {item} não está na mochila."

        current_equipped_item = None
        weight_to_add = item.weight

        if isinstance(item, WeaponModel):
            current_equipped_item = self.equipments.get("weapon")
        elif isinstance(item, ArmorModel):
            slot = item.type
            current_equipped_item = self.equipments.get(slot)

        if current_equipped_item:
            weight_to_add -= current_equipped_item.weight

        if self.weight + weight_to_add > self.carry_weight:
            return "Você não pode equipar este item, pois ele excede sua capacidade de carga."

        if isinstance(item, WeaponModel):
            self.attack_points += item.attack_points
            self.last_attack_damage += item.damage
            self.weight += item.weight

            if current_equipped_item:
                self.backpack.append(current_equipped_item)
                self.weight -= current_equipped_item.weight

            self.equipments["weapon"] = item

        elif isinstance(item, ArmorModel):
            slot = item.type
            if slot not in self.equipments:
                return f"Slot {slot} inválido para armadura."

            self.defense_points += item.def_points
            self.weight += item.weight

            if current_equipped_item:
                self.backpack.append(current_equipped_item)
                self.weight -= current_equipped_item.weight

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
            elif key == ord('\n'):  
                selected_item = self.backpack[current_row]
                result = self.equip_item(selected_item)
                stdscr.clear()
                stdscr.addstr(result + "\n")
                stdscr.addstr("Press any key to continue...")
                stdscr.getch()
            elif key == ord('q'):  
                break
            
            stdscr.refresh()

    def choose_character_class(self, stdscr: curses.window):
        classes = ["Fighter", "Rogue", "Wizard", "Cleric", "Paladin"]
        current_row = 0

        while True:
            stdscr.clear()
            stdscr.addstr("Use ↑ and ↓ to navigate, Enter to select a class, and 'q' to quit.\n\n")

            for idx, character_class in enumerate(classes):
                if idx == current_row:
                    stdscr.addstr(f"> {character_class}\n", curses.A_REVERSE)
                else:
                    stdscr.addstr(f"  {character_class}\n")

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(classes) - 1:
                current_row += 1
            elif key == ord('\n'): 
                selected_class = classes[current_row]
                break
            elif key == ord('q'):  
                return "Defaulting to Fighter."

            stdscr.refresh()

        if selected_class == "Fighter":
            self.character_class = Warrior()
        elif selected_class == "Rogue":
            self.character_class = Rogue()
        elif selected_class == "Wizard":
            self.character_class = Wizard()
        elif selected_class == "Cleric":
            self.character_class = Cleric()
        elif selected_class == "Paladin":
            self.character_class = Paladin()

        self.apply_class(self.character_class)

        return f"Class {selected_class} chosen successfully!"
        
        
    
    def apply_class(self, character_class: CharacterClass):
        """Applies a character class to the hero."""
        self.character_class = character_class
        self.health += character_class.health
        self.proficiencies.extend(character_class.proficiencies)
        self.abilities = character_class.abilities
        self.primary_stat = character_class.primary_stat
        self.spell_slots = character_class.spell_slots
        self.action_points += character_class.action_points if hasattr(character_class, 'action_points') else 0