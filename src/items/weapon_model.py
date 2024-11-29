from enums.rarity_enum import Rarity_Enum
from util.id_generator import IDGenerator
from enums.weapon_type_enum import Weapon_Type_Enum
class Weapon_model():
    
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: str, weapon_type: str, critical_hit_chance: float) -> None:
        self.item_id = IDGenerator.generate_id() 
        self.name = name
        self.attack_points = attack_points
        self.weight = weight
        self.value = value
        if(isinstance(rarity, Rarity_Enum)):
            self.rarity = rarity.name
        else:
            raise ValueError(f"Invalid rarity: {rarity}. Must be one of {list(Rarity_Enum)}")
        if(isinstance(weapon_type, Weapon_Type_Enum )):
            self.weapon_type = weapon_type.name
        else: 
            raise ValueError(f"Invalid weapon type: {weapon_type}. Must be one of{list(Weapon_Type_Enum)}")
        self.critical_hit_chance = critical_hit_chance
    
    def __str__(self) -> str:
        return f"{self.name} - {self.attack_points} ATK, {self.weight}kg, {self.value} gold ({self.rarity} {self.weapon_type})"

    def sell(self) -> int:
        print(f"You sold {self.name} for {self.value} gold.")
        return self.value