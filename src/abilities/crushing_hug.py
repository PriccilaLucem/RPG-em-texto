import random
from models.abilities_model import Ability_Model
from characters.hero import Hero
from models.enemy_model import EnemyModel
from typing import Union

class CrushingHug(Ability_Model):
    def __init__(self, damage_per_turn: int, escape_dc: int):
        super().__init__(name="Crushing Hug", cooldown=3)  # Define nome e cooldown
        self.damage_per_turn = damage_per_turn
        self.escape_dc = escape_dc
        self.grappled_target = None

    def use_ability(self, target: Union[EnemyModel, Hero]) -> str:
        if not self.is_ready():
            return f"{self.name} is on cooldown for {self.current_cooldown} more turns."

        if self.grappled_target is not None:
            return f"Already grappling {self.grappled_target.name}!"

        roll = random.randint(1, 20)
        if roll <= target.speed:
            return f"{target.name} escaped the grapple attempt!"
        
        self.grappled_target = target
        self.current_cooldown = self.cooldown
        return f"{target.name} is now grappled in a Crushing Hug!"

    def deal_damage(self) -> str:
        if self.grappled_target is None:
            return "No target is currently grappled."

        self.grappled_target.health_points -= self.damage_per_turn
        return f"{self.grappled_target.name} takes {self.damage_per_turn} crushing damage!"

    def release_target(self) -> str:
        if self.grappled_target is None:
            return "No target to release."

        target_name = self.grappled_target.name
        self.grappled_target = None
        return f"{target_name} has been released from the Crushing Hug."
