from enums.rarity_enum import Rarity_Enum
from util.id_generator import IDGenerator
from enums.weapon_type_enum import Weapon_Type_Enum
class Weapon_model():
    
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: str, weapon_type: str) -> None:
        self.item_id = IDGenerator.generate_id() 
        self.name = name
        self.attack_points = attack_points
        self.weight = weight
        self.value = value
        if(isinstance(rarity, Rarity_Enum)):
            self.rarity = rarity
        else:
            raise ValueError(f"Invalid rarity: {rarity}. Must be one of {list(Rarity_Enum)}")
        if(isinstance(weapon_type, Weapon_Type_Enum )):
            self.weapon_type = weapon_type
        else: 
            raise ValueError(f"Invalid weapon type: {weapon_type}. Must be one of{list(Weapon_Type_Enum)}")
    
    def __str__(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"Attack Points: {self.attack_points}\n"
            f"Weight: {self.weight} kg\n"
            f"Value: {self.value} gold\n"
            f"Rarity: {self.rarity}\n"
            f"Weapon Type: {self.weapon_type}\n"
        )
        
    def sell(self) -> int:
        print(f"You sold {self.name} for {self.value} gold.")
        return self.value