from enums.enemy_type_enum import EnemyType
from typing import List, Optional
from models.abilities_model import BaseAbility
from enums.immunity_enum import ImmunityEnum
from enums.weakness_enum import WeaknessEnum
from models.drop_model import DropModel
import random
from characters.hero import Hero
from models.item_model import Drops
from enums.rarity_enum import Rarity_Enum
import random
class EnemyModel:
    def __init__(self, 
                 name: str, 
                 type: EnemyType, 
                 attack_points: int, 
                 defense_points: int, 
                 attack_multiplier: float, 
                 critical_hit_chance: float, 
                 resistance_factor: float, 
                 health_points: int, 
                 speed: int, 
                 weakness: Optional[List[WeaknessEnum]] = None, 
                 immunities: Optional[List[ImmunityEnum]] = None, 
                 abilities: Optional[List[BaseAbility]] = None, 
                 exp_points: int = 0, 
                 drops: Optional[List[DropModel]] = None, 
                 location: str = "unknown",
                 level: int = 0
                 ) -> None:
        self.name = name
        
        if isinstance(type, EnemyType):
            self.type = type
        else:
            raise ValueError(f"Invalid type: {type}. Must be of type EnemyType.")

        self.attack_points = attack_points
        self.defense_points = defense_points
        self.attack_multiplier = attack_multiplier
        self.critical_hit_chance = critical_hit_chance
        self.resistance_factor = resistance_factor
        self.health_points = health_points
        self.speed = speed
        self.weakness = weakness or []
        self.immunities = immunities or []
        self.abilities = abilities or []
        self.exp_points = exp_points
        self.drops:List[Drops] = drops or []
        self.location = location
        self.level = level
        self.loot_collected = False 

    def use_skills(self, target) -> str:

        if not self.abilities:
            return f"{self.name} has no abilities to use."
        
        ability = random.choice(self.abilities)
        
        if hasattr(ability, 'use_ability'):
            return ability.use_ability(target)
        
        return f"{self.name} tries to use {ability} but it fails due to invalid implementation."

    def drop_items(self, main_character: Hero):
        rarity_probabilities = {
            Rarity_Enum.COMMON: 1,       # 100% chance
            Rarity_Enum.UNCOMMON: 0.5,   # 50% chance
            Rarity_Enum.RARE: 0.2,       # 20% chance
            Rarity_Enum.EPIC: 0.1,       # 10% chance
            Rarity_Enum.LEGENDARY: 0.05  # 5% chance
        }
        if not self.loot_collected:
            dropped_items = []
            for item in self.drops:
                if random.random() <= rarity_probabilities.get(item.rarity, 0):
                    dropped_items.append(item)
    
            if not dropped_items and self.drops:
                dropped_items.append(random.choice(self.drops))
            self.loot_collected = True
            main_character.backpack.extend(dropped_items)
            return f"{self.name} dropped: {[str(item) for item in dropped_items]}"
        
        return f"The loot from {self.name} has already been collected."
