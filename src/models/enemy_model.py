from enums.enemy_type_enum import EnemyType
from typing import List, Optional
from models.abilities_model import BaseAbility
from enums.immunity_enum import ImmunityEnum
from enums.weakness_enum import WeaknessEnum
from models.drop_model import DropModel
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
        self.drops = drops or []
        self.location = location
        self.level = level
    def use_skills(self, target) -> str:

        if not self.abilities:
            return f"{self.name} has no abilities to use."
        
        ability = random.choice(self.abilities)
        
        if hasattr(ability, 'use_ability'):
            return ability.use_ability(target)
        
        return f"{self.name} tries to use {ability} but it fails due to invalid implementation."
