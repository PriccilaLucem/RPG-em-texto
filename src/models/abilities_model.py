from util.id_generator import IDGenerator
from enums.skill_type_enum import SkillTypeEnum

class BaseAbility:
    def __init__(self, name: str, cooldown: int, description, level=0):
        self.id = IDGenerator.generate_id()
        self.name = name
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.level = level
        self.description = description
    def reduce_cooldown(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def is_ready(self) -> bool:
        return self.current_cooldown == 0

    def apply(self, caster, target):
        raise NotImplementedError("Subclasses must implement the apply method")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "cooldown": self.cooldown,
            "current_cooldown": self.current_cooldown,
            "level": self.level,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            cooldown=data["cooldown"],
            description=data["description"],
            level=data.get("level", 0),
        )


class DamageAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, damage: int, description, level=0):
        super().__init__(name, cooldown, description, level)
        self.type = SkillTypeEnum.DAMAGE
        self.damage = damage + (level * 0.5)

    def apply(self, _, target):
        target.health_points = max(0, target.health_points - self.damage)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "type": self.type.name,
            "damage": self.damage
        })
        return base

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            cooldown=data["cooldown"],
            damage=data["damage"],
            description=data["description"],
            level=data.get("level", 0)
        )


class HealAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, effect_value: int, description, level=0):
        super().__init__(name, cooldown, description, level)
        self.type = SkillTypeEnum.HEAL
        self.effect_value = effect_value

    def apply(self, caster, _):
        caster.health_points = min(caster.max_hp, caster.health_points + self.effect_value)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "type": self.type.name,
            "effect_value": self.effect_value
        })
        return base

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            cooldown=data["cooldown"],
            effect_value=data["effect_value"],
            description=data["description"],
            level=data.get("level", 0)
        )


class BuffAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, effect_value: int, description, level=0, buff_type="attack"):
        super().__init__(name, cooldown, description, level)
        self.type = SkillTypeEnum.BUFF
        self.effect_value = effect_value
        self.buff_type = buff_type

    def apply(self, caster, _):
        if self.buff_type == "attack":
            caster.attack_points += self.effect_value
        elif self.buff_type == "defense":
            caster.defense_points += self.effect_value
        elif self.buff_type == "both":
            caster.attack_points += self.effect_value
            caster.defense_points += self.effect_value

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "type": self.type.name,
            "effect_value": self.effect_value,
            "buff_type": self.buff_type
        })
        return base

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            cooldown=data["cooldown"],
            effect_value=data["effect_value"],
            description=data["description"],
            level=data.get("level", 0),
            buff_type=data.get("buff_type", "attack")
        )


class DebuffAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, effect_value: int, description, level=0, debuff_type="attack"):
        super().__init__(name, cooldown, description, level)
        self.type = SkillTypeEnum.DEBUFF
        self.effect_value = effect_value
        self.debuff_type = debuff_type

    def apply(self, caster, target):
        if self.debuff_type == "attack":
            target.attack_points = max(0, target.attack_points - self.effect_value)
        elif self.debuff_type == "defense":
            target.defense_points = max(0, target.defense_points - self.effect_value)
        elif self.debuff_type == "both":
            target.attack_points = max(0, target.attack_points - self.effect_value)
            target.defense_points = max(0, target.defense_points - self.effect_value)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "type": self.type.name,
            "effect_value": self.effect_value,
            "debuff_type": self.debuff_type
        })
        return base

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            cooldown=data["cooldown"],
            effect_value=data["effect_value"],
            description=data["description"],
            level=data.get("level", 0),
            debuff_type=data.get("debuff_type", "attack")
        )


class UtilityAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, description, effect_value: int = 0, level=0):
        super().__init__(name, cooldown, description, level)
        self.type = SkillTypeEnum.UTILITY
        self.effect_value = effect_value

    def apply(self, caster, target=None):
        raise NotImplementedError("Subclasses devem implementar o método 'apply'.")

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "type": self.type.name,
            "effect_value": self.effect_value
        })
        return base

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            cooldown=data["cooldown"],
            description=data["description"],
            effect_value=data.get("effect_value", 0),
            level=data.get("level", 0)
        )