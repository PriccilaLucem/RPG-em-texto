from enum import Enum
from util.id_generator import IDGenerator
from enums.rarity_enum import Rarity_Enum
from enums.armor_type_enum import Armor_Type_Enum
from enums.weapon_type_enum import Weapon_Type_Enum

class ItemModel:
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float) -> None:
        self.item_id = IDGenerator.generate_id() 
        self.name = name
        self.value = value
        if isinstance(rarity, Rarity_Enum):
            self.rarity = rarity.name.lower()
        else:
            raise ValueError(f"Invalid rarity: {rarity}. Must be one of {list(Rarity_Enum)}")
        self.weight = weight 

    def sell(self) -> int:
        print(f"You sold {self.name} for {self.value} gold.")
        return self.value

class ArmorModel(ItemModel):
    def __init__(self, name: str, def_points: int, weight: float, value: int, rarity: Rarity_Enum, armor_type: Armor_Type_Enum) -> None:
        super().__init__(name, value, rarity, weight)
        if isinstance(armor_type, Armor_Type_Enum):
            self.type = armor_type.name.lower()
        else:
            raise ValueError(f"Invalid armor type: {armor_type}. Must be one of {list(Armor_Type_Enum)}")
        self.def_points = def_points

    def __str__(self): 
        return f"{self.name} - {self.def_points} DEF, {self.weight}kg, {self.value} gold ({self.rarity} {self.type})"

class HeavyArmor(ArmorModel):
    def __init__(self, name: str, def_points: int, weight: float, value: int, rarity: Rarity_Enum, armor_type: Armor_Type_Enum) -> None:
        super().__init__(name, def_points, weight, value, rarity, armor_type)
        self.armor_class = "Heavy"

class LightArmor(ArmorModel):
    def __init__(self, name: str, def_points: int, weight: float, value: int, rarity: Rarity_Enum, armor_type: Armor_Type_Enum) -> None:
        super().__init__(name, def_points, weight, value, rarity, armor_type)
        self.armor_class = "Light"


class WeaponModel(ItemModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, weapon_type: Weapon_Type_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight)
        if isinstance(weapon_type, Weapon_Type_Enum):
            self.weapon_type = weapon_type.name
        else: 
            raise ValueError(f"Invalid weapon type: {weapon_type}. Must be one of {list(Weapon_Type_Enum)}")
        self.attack_points = attack_points
        self.critical_hit_chance = critical_hit_chance

    def __str__(self) -> str:
        return f"{self.name} - {self.attack_points} ATK, {self.weight}kg, {self.value} gold ({self.rarity} {self.weapon_type})"


class Sword(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, attack_points, weight, value, rarity, Weapon_Type_Enum.SWORD, critical_hit_chance)

class Axe(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, attack_points, weight, value, rarity, Weapon_Type_Enum.AXE, critical_hit_chance)

class Bow(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, attack_points, weight, value, rarity, Weapon_Type_Enum.BOW, critical_hit_chance)

class Dagger(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, attack_points, weight, value, rarity, Weapon_Type_Enum.DAGGER, critical_hit_chance)

def sell_item(item: ItemModel) -> int:
    return item.sell()
