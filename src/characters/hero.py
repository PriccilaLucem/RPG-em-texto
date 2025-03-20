from typing import Any, List, Union, Optional, Dict
from quests.quests import Quests, CollectableQuest
from models.item_model import ArmorModel, WeaponModel, ItemsUsedToCraft, Food
from models.abilities_model import BaseAbility
from models.character_class_model import CharacterClass
import curses
from classes.cleric import Cleric
from classes.paladin import Paladin
from classes.rogue import Rogue
from classes.warrior import Warrior
from classes.wizard import Wizard
from util.classes import ABILITY_CLASSES
class Hero():

    def __init__(self) -> None:
        self.name: str = "Hero" 
        self.health_points:int = 50
        self.max_hp:int = 50
        self.gold:int = 1000000
        self.backpack:List[Union[WeaponModel, ArmorModel, Food, ItemsUsedToCraft]] = []
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
        self.quests: List[Union[Quests, CollectableQuest]] = [] 
        self.concluded_quests: List[Union[Quests, CollectableQuest]] = []
        self.speed = 10 
        self.attack_multiplier = 1
        self.proficiencies = []
        self.extra_actions = 0
        self.dodge_chance = 0
        self.health = 100
        self.last_attack_damage = 0
        self.carry_weight = 50
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
    
    def append_quests(self, quest:Union[Quests, CollectableQuest]):
        self.quests.append(quest)
        
    def init_a_quest(self, quest:Quests):
        self.quests.append(quest)
    
    def conclude_quests(self, quest: Quests):
        if not quest:
            raise ValueError("Quest cannot be None.")
        if quest not in self.quests:
            raise ValueError("Quest is not part of the active quests list.")

        self.gold += quest.gold_given
        self.concluded_quests.append(quest)
        self.quests.remove(quest)
        if self.experience + quest.xp_given < self.next_level_xp:
            self.experience += quest.xp_given
        else:
            remaining_xp = (self.experience + quest.xp_given) - self.next_level_xp
            self.level_up()
            self.experience = remaining_xp

    def equip_item(self, item: Union[ArmorModel, WeaponModel]) -> str:
        if item not in self.backpack:
            return f"Item {item.name} não está na mochila."

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

        proficiency_bonus = 2 if any(p in self.proficiencies for p in item.proeficiency) else -5

        if isinstance(item, WeaponModel):
            self.attack_points += item.attack_points + proficiency_bonus
            self.last_attack_damage += item.critical_hit_chance
            self.weight += item.weight

            if current_equipped_item:
                self.backpack.append(current_equipped_item)
                self.weight -= current_equipped_item.weight

            self.equipments["weapon"] = item

        elif isinstance(item, ArmorModel):
            slot = item.type
            if slot not in self.equipments:
                return f"Slot {slot} inválido para armadura."

            self.defense_points += item.def_points + proficiency_bonus
            self.weight += item.weight

            if current_equipped_item:
                self.backpack.append(current_equipped_item)
                self.weight -= current_equipped_item.weight

            self.equipments[slot] = item

        self.backpack.remove(item)
        return f"Item {item.name} equipado com sucesso!"

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
        self.health += character_class.health
        self.max_hp += character_class.health
        self.proficiencies.extend(character_class.proficiencies)
        self.abilities = character_class.abilities
        self.primary_stat = character_class.primary_stat
        self.spell_slots = character_class.spell_slots 
    
    def add_to_inventory(self, item):
        self.backpack.append(item)
        self.weight += item.weight

    def remove_items_from_backpack(self, items_to_be_collected):
        for item, quantity in items_to_be_collected:
            available_quantity = sum(1 for i in self.backpack if i == item)
            if available_quantity < quantity:
                raise ValueError(f"Not enough {item.name} in the backpack. Needed {quantity}, found {available_quantity}.")

        for item, quantity in items_to_be_collected:
            count = 0
            for i in range(len(self.backpack) - 1, -1, -1):  
                if self.backpack[i] == item:
                    self.backpack.pop(i)
                    self.weight -= item.weight
                    count += 1
                    if count == quantity:  
                        break
    
    def find_quest_by_id(self, quest_id: int):
        return next((quest for quest in self.quests if quest.id == quest_id), None)
    
    def to_dict(self):
        return {
            "name": self.name,
            "health_points": self.health_points,
            "max_hp": self.max_hp,
            "gold": self.gold,
            "backpack": [item.to_dict() for item in self.backpack] if self.backpack else [],
            "abilities":[ability.to_dict() if hasattr(ability, 'to_dict') else ability 
            for ability in self.abilities
            ] if self.abilities else [],
            "equipments": {
                key: item.to_dict() if hasattr(item, 'to_dict') else item
                for key, item in (self.equipments or {}).items()
            },
            "character_class": self.character_class.to_dict() if self.character_class else None,
            "experience": self.experience,
            "next_level_xp": self.next_level_xp,
            "attack_points": self.attack_points,
            "defense_points": self.defense_points,
            "level": self.level,
            "critical_hit_chance": self.critical_hit_chance,
            "resistance_factor": self.resistance_factor,
            "quests": [quest.to_dict() for quest in self.quests] if self.quests else [],
            "concluded_quests": [quest.to_dict() for quest in self.concluded_quests] if self.concluded_quests else [],
            "speed": self.speed,
            "attack_multiplier": self.attack_multiplier,
            "proficiencies": self.proficiencies,
            "extra_actions": self.extra_actions,
            "dodge_chance": self.dodge_chance,
            "health": self.health,
            "last_attack_damage": self.last_attack_damage,
            "carry_weight": self.carry_weight,
            "weight": self.weight,
        }

    @classmethod
    def from_dict(cls, data):
        hero = cls()
        hero.name = data.get("name")
        hero.health_points = data.get("health_points")
        hero.max_hp = data.get("max_hp")
        hero.gold = data.get("gold")

        # Process backpack items
        hero.backpack = [
            WeaponModel.from_dict(item) if isinstance(item, dict) and "attack_points" in item else
            ArmorModel.from_dict(item) if isinstance(item, dict) and "def_points" in item else
            Food.from_dict(item) if isinstance(item, dict) and "health_recovery" in item else
            ItemsUsedToCraft.from_dict(item)
            for item in data.get("backpack", [])
        ]

        # Process abilities
        hero.abilities = [
               ABILITY_CLASSES.get(ability.get("type")).from_dict(ability)
               if isinstance(ability, dict) and ability.get("type") in ABILITY_CLASSES
               else ability
               for ability in data.get("abilities", [])] if data.get("abilities") else []

        # Process equipments
        hero.equipments = {
            key: WeaponModel.from_dict(item) if item and "damage" in item else
            ArmorModel.from_dict(item) if item else None
            for key, item in data.get("equipments", {}).items()
        }

        # Process character class
        hero.character_class = CharacterClass.from_dict(data["character_class"]) if data.get("character_class") else None

        # Process basic attributes
        hero.experience = data.get("experience")
        hero.next_level_xp = data.get("next_level_xp")
        hero.attack_points = data.get("attack_points")
        hero.defense_points = data.get("defense_points")
        hero.level = data.get("level")
        hero.critical_hit_chance = data.get("critical_hit_chance")
        hero.resistance_factor = data.get("resistance_factor")

        # Process quests
        hero.quests = [
            Quests.from_dict(quest) if "items_to_be_collected" not in quest else CollectableQuest.from_dict(quest)
            for quest in data.get("quests", [])
        ]

        # Process concluded quests
        hero.concluded_quests = [
            Quests.from_dict(quest) if "items_to_be_collected" not in quest else CollectableQuest.from_dict(quest)
            for quest in data.get("concluded_quests", [])
        ]

        # Process additional attributes
        hero.speed = data.get("speed")
        hero.attack_multiplier = data.get("attack_multiplier")
        hero.proficiencies = data.get("proficiencies")
        hero.extra_actions = data.get("extra_actions")
        hero.dodge_chance = data.get("dodge_chance")
        hero.health = data.get("health")
        hero.last_attack_damage = data.get("last_attack_damage")
        hero.carry_weight = data.get("carry_weight")
        hero.weight = data.get("weight")

        return hero