from enums.enemy_type_enum import EnemyTypeEnum
from typing import List, Optional, Dict
from models.abilities_model import BaseAbility
from enums.immunity_enum import ImmunityEnum
from enums.weakness_enum import WeaknessEnum
from models.item_model import ItemsUsedToCraft
import random
from characters.hero import Hero
from enums.rarity_enum import Rarity_Enum

class EnemyModel:
    def __init__(self, 
                 name: str, 
                 type: EnemyTypeEnum, 
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
                 drops: Optional[List[ItemsUsedToCraft]] = None, 
                 location: str = "unknown",
                 level: int = 0
                 ) -> None:
        self.name = name
        if isinstance(type, EnemyTypeEnum):
            self.type = type
        else:
            raise ValueError(f"Invalid type: {type}. Must be of type EnemyTypeEnum.")

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
        self.drops: List[ItemsUsedToCraft] = drops or []
        self.location = location
        self.level = level
        self.loot_collected = False  

    def use_skills(self, target) -> str:
        if not self.abilities:
            return f"{self.name} has no abilities to use."
        
        ability = random.choice(self.abilities)
        
        if callable(getattr(ability, 'use_ability', None)):
            return ability.use_ability(target)
        
        return f"{self.name} tries to use {ability} but it fails due to invalid implementation."

    def drop_items(self, main_character: Hero):
        rarity_probabilities = {
            Rarity_Enum.COMMON: 1.0,
            Rarity_Enum.UNCOMMON: 0.5,
            Rarity_Enum.RARE: 0.2,
            Rarity_Enum.EPIC: 0.1,
            Rarity_Enum.LEGENDARY: 0.05
        }

        if self.loot_collected:
            return f"The loot from {self.name} has already been collected."

        dropped_items = [item for item in self.drops if random.random() <= rarity_probabilities.get(item.rarity, 0)]

        for item in dropped_items:
            main_character.add_to_inventory(item)

        self.loot_collected = True
        return f"{self.name} dropped: {[str(item) for item in dropped_items]}" if dropped_items else f"{self.name} dropped nothing."

    @classmethod
    def from_dict(cls, data: Dict) -> "EnemyModel":
        return cls(
            name=data["name"],
             type=EnemyTypeEnum[data["type"]],
             attack_points=data["attack_points"],
             defense_points=data["defense_points"],
             attack_multiplier=data["attack_multiplier"],
             critical_hit_chance=data["critical_hit_chance"],
             resistance_factor=data["resistance_factor"],
             health_points=data["health_points"],
             speed=data["speed"],
             weakness = [WeaknessEnum[w.upper()] for w in data.get("weakness", []) if w.upper() in WeaknessEnum.__members__],
             immunities = [ImmunityEnum[i.upper()] for i in data.get("immunities", []) if i.upper() in ImmunityEnum.__members__],
             abilities=[BaseAbility.from_dict(ability) for ability in data.get("abilities", [])],
             exp_points=data["exp_points"],
             drops=[ItemsUsedToCraft.from_dict(item) for item in data.get("drops", [])],
             location=data.get("location", "unknown"),
             level=data["level"]
         )
    
    def to_dict(self) -> Dict:
        """Convert the EnemyModel instance to a dictionary."""
        return {
            "name": self.name,
            "type": self.type.name if hasattr(self.type, 'name') else str(self.type),
            "attack_points": self.attack_points,
            "defense_points": self.defense_points,
            "attack_multiplier": self.attack_multiplier,
            "critical_hit_chance": self.critical_hit_chance,
            "resistance_factor": self.resistance_factor,
            "health_points": self.health_points,
            "speed": self.speed,
            "weakness": [w.name for w in self.weakness] if self.weakness else [],
            "immunities": [i.name for i in self.immunities] if self.immunities else [],
            "abilities": [ability.to_dict() for ability in self.abilities if hasattr(ability, 'to_dict')] if self.abilities else [],
            "exp_points": self.exp_points,
            "drops": [item.to_dict() for item in self.drops if hasattr(item, 'to_dict')] if self.drops else [],
            "location": self.location,
            "level": self.level,
            "loot_collected": self.loot_collected
        }