from characters.hero import Hero
from models.enemy_model import Enemy_model
from typing import Union
import random

def attack(attacker: Union[Enemy_model, Hero], defenser : Union[Enemy_model, Hero]) -> int:

    base_damage = attacker.attack_points - defenser.defense_points
    base_damage *= attacker.attack_multiplier

    if base_damage < 0:
        base_damage = 0


    base_damage *= defenser.resistance_factor
    roll = random.randint(1,20)
    if roll < attacker.critical_hit_chance:
        critical_damage = base_damage * 1.5
        return int(critical_damage)

    return int(base_damage)

def defend(defender: Union[Enemy_model, Hero], attacker: Union[Enemy_model, Hero]) -> int:
    
    base_damage = attacker.attack_points - defender.defense_points
    base_damage *= attacker.attack_multiplier

    if base_damage < 0:
        base_damage = 0

    mitigated_damage = base_damage * defender.resistance_factor

    if random.randint(1,20) < defender.critical_hit_chance:
        mitigated_damage *= 0.5  
    return int(mitigated_damage)
