from util.id_generator import IDGenerator
from enum.rarity_enum import Rarity_Enum
class ArmorModel:
    def __init__(self, name: str, def_points: int, weight: float, value: int, rarity: str) -> None:
        self.item_id = IDGenerator.generate_id() 
        self.name = name
        self.def_points = def_points
        self.weight = weight
        self.value = value
        if isinstance(rarity, Rarity_Enum):
            self.rarity = rarity
        else:
            raise ValueError((f"Invalid rarity: {rarity}. Must be one of {list(Rarity_Enum)}"))


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
