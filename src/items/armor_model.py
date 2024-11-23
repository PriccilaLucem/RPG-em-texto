from util.id_generator import IDGenerator
from enums.rarity_enum import Rarity_Enum
from enums.armor_type_enum import Armor_Type_Enum

class ArmorModel:
    def __init__(self, name: str, def_points: int, weight: float, value: int, rarity: Rarity_Enum, type: Armor_Type_Enum) -> None:
        self.item_id = IDGenerator.generate_id() 
        self.name = name
        self.def_points = def_points
        self.weight = weight
        self.value = value
        if isinstance(rarity, Rarity_Enum):
            self.rarity = rarity
        else:
            raise ValueError((f"Invalid rarity: {rarity}. Must be one of {list(Rarity_Enum)}"))
        if isinstance(type, Armor_Type_Enum):
            self.type = type
        else:
            raise ValueError((f"Invalid armor_type: {type}. Must be one of {list(Armor_Type_Enum)}"))
            

    def __str__(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"Defense Points: {self.def_points}\n"
            f"Weight: {self.weight} kg\n"
            f"Value: {self.value} gold\n"
            f"Rarity: {self.rarity}\n"
        )
        
    def sell(self) -> int:
        print(f"You sold {self.name} for {self.value} gold.")
        return self.value
