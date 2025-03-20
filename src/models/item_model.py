from enums.proeficiency_enum import Proeficiency_Enum
from util.id_generator import IDGenerator
from enums.rarity_enum import Rarity_Enum
from enums.armor_type_enum import Armor_Type_Enum
from enums.weapon_type_enum import Weapon_Type_Enum
from typing import List

class ItemModel:
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float) -> None:
        self.item_id = IDGenerator.generate_id()  # Gera um ID automaticamente
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

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "value": self.value,
            "rarity": self.rarity.name if self.rarity else None,  
            "weight": self.weight
        }

    @classmethod
    def from_dict(cls, data: dict):
        rarity = Rarity_Enum[data["rarity"]]
        
        item = cls(
            name=data["name"],
            value=data["value"],
            rarity=rarity,
            weight=data["weight"]
        )
        
        if "item_id" in data:
            item.item_id = data["item_id"]
        
        return item

    def __str__(self):
        return f"{self.name} (Value: {self.value} Gold, Weight: {self.weight}kg, Rarity: {self.rarity})"

class ArmorModel(ItemModel):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, proeficiency: List[Proeficiency_Enum], armor_type: Armor_Type_Enum, def_points: int) -> None:
        super().__init__(name, value, rarity, weight)        
        if isinstance(armor_type, Armor_Type_Enum):
            self.armor_type = armor_type
        else:
            raise ValueError(f"Invalid armor type: {armor_type}. Must be one of {list(Armor_Type_Enum)}")
        self.def_points = def_points
        self.proeficiency = proeficiency

    def __str__(self):
        return f"{self.name} (DEF: {self.def_points}, Value: {self.value} Gold, Weight: {self.weight}kg, Rarity: {self.rarity}, Type: {self.type})"
    
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "def_points": self.def_points,
            "proeficiency": [p.name for p in self.proeficiency],
            "armor_type": self.armor_type.name
        })
        return base_dict

 
    @classmethod
    def from_dict(cls, data: dict):
        item = super().from_dict(data)
        item.proeficiency = [Proeficiency_Enum[p] for p in data["proeficiency"]]
        item.armor_type = Armor_Type_Enum[data["armor_type"]]
        item.def_points = data["def_points"]
        return item

class HeavyArmor(ArmorModel):
    def __init__(self, name: str, def_points: int, weight: float, value: int, rarity: Rarity_Enum, armor_type: Armor_Type_Enum) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.HEAVY_ARMOR], armor_type, def_points)
        self.armor_class = "Heavy"

    def __str__(self):
        return f"Heavy Armor: {self.name} (DEF: {self.def_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Armor Class: {self.armor_class})"

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "armor_class": self.armor_class
        })
        return base_dict

    @classmethod
    def from_dict(cls, data: dict):
        armor_type = Armor_Type_Enum[data["armor_type"]]
        
        rarity = Rarity_Enum[data["rarity"]]
        
        heavy_armor = cls(
            name=data["name"],
            def_points=data["def_points"],
            weight=data["weight"],
            value=data["value"],
            rarity=rarity,
            armor_type=armor_type
        )
        return heavy_armor

class LightArmor(ArmorModel):
    def __init__(self, name: str, def_points: int, weight: float, value: int, rarity: Rarity_Enum, armor_type: Armor_Type_Enum) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.LIGHT_ARMOR], armor_type, def_points)
        self.armor_class = "Light"

    def __str__(self):
        return f"Light Armor: {self.name} (DEF: {self.def_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Armor Class: {self.armor_class})"

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "armor_class": self.armor_class
        })
        return base_dict

    @classmethod
    def from_dict(cls, data: dict):
        armor_type = Armor_Type_Enum[data["armor_type"]]
        
        rarity = Rarity_Enum[data["rarity"]]
        
        light_armor = cls(
            name=data["name"],
            def_points=data["def_points"],
            weight=data["weight"],
            value=data["value"],
            rarity=rarity,
            armor_type=armor_type
        )
        
        return light_armor

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
        
    def __str__(self):
        return f"{self.name} (ATK: {self.attack_points}, Value: {self.value} Gold, Weight: {self.weight}kg, Rarity: {self.rarity}, Type: {self.weapon_type}, Crit: {self.critical_hit_chance}%)"

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "weapon_type": self.weapon_type,
            "attack_points": self.attack_points,
            "critical_hit_chance": self.critical_hit_chance,
            "proeficiency": [p.name for p in self.proeficiency]
        })
        return base_dict

    @classmethod
    def from_dict(cls, data: dict):
        rarity  = Rarity_Enum[data["rarity"]]
        return cls(
            name=data["name"],
            value=data["value"],
            rarity=rarity,
            weight=data["weight"],
            critical_hit_chance = data["critical_hit_chance"],
            attack_points = data["attack_points"]
        )
    

class Sword(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.SWORDS], Weapon_Type_Enum.SWORD, attack_points, critical_hit_chance)

    def __str__(self):
        return f"Sword: {self.name} (ATK: {self.attack_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Critical Hit Chance: {self.critical_hit_chance}%)"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class Axe(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.AXES], Weapon_Type_Enum.AXE, attack_points, critical_hit_chance)

    def __str__(self):
        return f"Axe: {self.name} (ATK: {self.attack_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Critical Hit Chance: {self.critical_hit_chance}%)"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class Bow(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.BOWS], Weapon_Type_Enum.BOW, attack_points, critical_hit_chance)

    def __str__(self):
        return f"Bow: {self.name} (ATK: {self.attack_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Critical Hit Chance: {self.critical_hit_chance}%)"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class Dagger(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.DAGGERS], Weapon_Type_Enum.DAGGER, attack_points, critical_hit_chance)

    def __str__(self):
        return f"Dagger: {self.name} (ATK: {self.attack_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Critical Hit Chance: {self.critical_hit_chance}%)"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class Shield(ArmorModel):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, proeficiency: List[Proeficiency_Enum], def_points: int) -> None:
        super().__init__(name, value, rarity, weight, proeficiency, Armor_Type_Enum.SHIELD, def_points)

    def __str__(self):
        return f"Shield: {self.name} (DEF: {self.def_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity})"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class LightShield(Shield):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, def_points: int) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.SHIELDS, Proeficiency_Enum.LIGHT_ARMOR], def_points)

    def __str__(self):
        return f"Light Shield: {self.name} (DEF: {self.def_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity})"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class HeavyShield(Shield):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, def_points: int) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.SHIELDS, Proeficiency_Enum.HEAVY_ARMOR], def_points)

    def __str__(self):
        return f"Heavy Shield: {self.name} (DEF: {self.def_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity})"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class Mace(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.MACES], Weapon_Type_Enum.CLUB, attack_points, critical_hit_chance)

    def __str__(self):
        return f"Mace: {self.name} (ATK: {self.attack_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Critical Hit Chance: {self.critical_hit_chance}%)"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class Wand(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.WANDS], Weapon_Type_Enum.WAND, attack_points, critical_hit_chance)

    def __str__(self):
        return f"Wand: {self.name} (ATK: {self.attack_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Critical Hit Chance: {self.critical_hit_chance}%)"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class Spellbook(ItemModel):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float) -> None:
        super().__init__(name, value, rarity, weight)
        self.proeficiency = [Proeficiency_Enum.SPELLBOOKS]

    def __str__(self):
        return f"Spellbook: {self.name} (Value: {self.value} Gold, Weight: {self.weight}kg, Rarity: {self.rarity})"

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "proeficiency": [p.name for p in self.proeficiency]
        })
        return base_dict

    @classmethod
    def from_dict(cls, data: dict):
        rarity = Rarity_Enum[data["rarity"]]
        return cls(data["name"], data["value"], rarity, data["weight"])


class Crossbow(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.BOWS], Weapon_Type_Enum.CROSSBOW, attack_points, critical_hit_chance)

    def __str__(self):
        return f"Crossbow: {self.name} (ATK: {self.attack_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Critical Hit Chance: {self.critical_hit_chance}%)"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class Club(WeaponModel):
    def __init__(self, name: str, attack_points: int, weight: float, value: int, rarity: Rarity_Enum, critical_hit_chance: float) -> None:
        super().__init__(name, value, rarity, weight, [Proeficiency_Enum.MACES], Weapon_Type_Enum.CLUB, attack_points, critical_hit_chance)

    def __str__(self):
        return f"Club: {self.name} (ATK: {self.attack_points}, Weight: {self.weight}kg, Value: {self.value} Gold, Rarity: {self.rarity}, Critical Hit Chance: {self.critical_hit_chance}%)"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class ItemsUsedToCraft(ItemModel):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float) -> None:
        super().__init__(name, value, rarity, weight)

    def __str__(self):
        return f"{self.name} (Rarity: {self.rarity}, Weight: {self.weight}kg, Value: {self.value} Gold)"

    def to_dict(self) -> dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: dict):
        return super().from_dict(data)


class Food(ItemsUsedToCraft):
    def __init__(self, name: str, value: int, rarity: Rarity_Enum, weight: float, health_recovery: str) -> None:
        super().__init__(name, value, rarity, weight)
        self.health_recovery = health_recovery

    def __str__(self):
        return f"Food: {self.name} (Value: {self.value} Gold, Weight: {self.weight}kg, Rarity: {self.rarity}, Health Recovery: {self.health_recovery})"

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "health_recovery": self.health_recovery
        })
        return base_dict

    @classmethod
    def from_dict(cls, data: dict):
        rarity = Rarity_Enum[data["rarity"]]
        return cls(data["name"], data["value"], rarity, data["weight"], data["health_recovery"])