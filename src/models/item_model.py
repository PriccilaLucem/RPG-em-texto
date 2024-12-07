from enums.proeficiency_enum import Proeficiency_Enum
from util.id_generator import IDGenerator
from enums.rarity_enum import Rarity_Enum
from enums.armor_type_enum import Armor_Type_Enum
from enums.weapon_type_enum import Weapon_Type_Enum
from typing import List

# Item father class

class ItemModel:
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float) -> None:
        self.item_id = IDGenerator.generate_id() 
        self.name = name
        self.value = value
        if isinstance(rarity, Rarity_Enum):
            self.rarity = rarity
        else:
            raise ValueError(f"Invalid rarity: {rarity}. Must be one of {list(Rarity_Enum)}")
        self.weight = weight 

    def sell(self) -> int:
        print(f"You sold {self.name} for {self.value} gold.")
        return self.value

# Weapons and armors 

class ArmorModel(ItemModel):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, proeficiency: List[Proeficiency_Enum], armor_type: Armor_Type_Enum, def_points: int) -> None:
        super().__init__(name, value, rarity, weight)        
        if isinstance(armor_type, Armor_Type_Enum):
            self.type = armor_type.name.lower()
        else:
            raise ValueError(f"Invalid armor type: {armor_type}. Must be one of {list(Armor_Type_Enum)}")
        self.def_points = def_points
        self.proeficiency = proeficiency


    def __str__(self): 
        return f"{self.name} - {self.def_points} DEF, {self.weight}kg, {self.value} gold ({self.rarity} {self.type})"

class HeavyArmor(ArmorModel):
    def __init__(self, name: str, def_points:int, weight:float, value: int, rarity: Rarity_Enum, armor_type: Armor_Type_Enum) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.HEAVY_ARMOR], armor_type, def_points)
        self.armor_class = "Heavy"

class LightArmor(ArmorModel):
    def __init__(self, name: str, def_points:int, weight:float, value: int, rarity: Rarity_Enum, armor_type: Armor_Type_Enum) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.LIGHT_ARMOR], armor_type, def_points)
        self.armor_class = "Light"


class WeaponModel(ItemModel):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, proeficiency: List[Proeficiency_Enum], weapon_type: Weapon_Type_Enum, attack_points: int, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight)
        if isinstance(weapon_type, Weapon_Type_Enum):
            self.weapon_type = weapon_type.name
        else: 
            raise ValueError(f"Invalid weapon type: {weapon_type}. Must be one of {list(Weapon_Type_Enum)}")
        self.attack_points = attack_points
        self.critical_hit_chance = critical_hit_chance
        self.proeficiency = proeficiency

    def __str__(self) -> str:
        return f"{self.name} - {self.attack_points} ATK, {self.weight}kg, {self.value} gold ({self.rarity} {self.weapon_type})"

class Sword(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.SWORDS], Weapon_Type_Enum.SWORD, attack_points, critical_hit_chance)

class Axe(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.AXES], Weapon_Type_Enum.AXE, attack_points, critical_hit_chance)

class Bow(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.BOWS], Weapon_Type_Enum.BOW, attack_points, critical_hit_chance)

class Dagger(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.DAGGERS], Weapon_Type_Enum.DAGGER, attack_points, critical_hit_chance)

def sell_item(item: ItemModel) -> int:
    return item.sell()

class Shield(ArmorModel):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, proeficiency: List[Proeficiency_Enum], def_points: int) -> None:
        super().__init__(name, value, rarity, weight, proeficiency, Armor_Type_Enum.SHIELD, def_points)

class LightShield(Shield):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, def_points: int) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.SHIELDS, Proeficiency_Enum.LIGHT_ARMOR], def_points)

class HeavyShield(Shield):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, def_points: int) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.SHIELDS, Proeficiency_Enum.HEAVY_ARMOR], def_points)

class Mace(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, attack_points, weight, value, [Proeficiency_Enum.MACES], rarity, Weapon_Type_Enum.CLUB, critical_hit_chance)
class Wand(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, attack_points, weight, value, [Proeficiency_Enum.WANDS], rarity, Weapon_Type_Enum.WAND, critical_hit_chance)

class Spellbook(ItemModel):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float) -> None:
        super().__init__(name, value, rarity, weight)
        self.proeficiency =  [Proeficiency_Enum.SPELLBOOKS]
    def __str__(self) -> str:
        return f"{self.name} - {self.weight}kg, {self.value} gold ({self.rarity} Spellbook)"

class Crossbow(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, attack_points, weight, value, [Proeficiency_Enum.BOWS], rarity, Weapon_Type_Enum.CROSSBOW, critical_hit_chance)

class Club(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, attack_points, weight, value, [Proeficiency_Enum.MACES], rarity, Weapon_Type_Enum.CLUB, critical_hit_chance)


# Items witch will be used for crafting or to sail
class ItemsUsedToCraft(ItemModel):
    def __init__(self, name, value, rarity, weight):
        super().__init__(name, value, rarity, weight)

    def __str__(self):
        return f"{self.name} (Rarity: {self.rarity}, Weight: {self.weight})"

class Ores(ItemsUsedToCraft):
    def __init__(self, name, value, rarity, weight):
        super().__init__(name, value, rarity, weight)

class Drops(ItemsUsedToCraft):
    def __init__(self, name, value, rarity, weight):
        super().__init__(name, value, rarity, weight)