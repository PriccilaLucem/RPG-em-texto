from util.id_generator import IDGenerator
from enums.skill_type_enum import SkillTypeEnum

class BaseAbility():
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

    def __str__(self) -> str:
        return f"{self.id}: {self.name} (Cooldown: {self.cooldown}, Nível: {self.level})"


class DamageAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, damage: int, description, level=0):
        super().__init__(name, cooldown, level, description)
        self.type = SkillTypeEnum.DAMAGE
        self.damage = damage + (level * 0.5)

    def apply(self, _, target):
        target.health_points = max(0, target.health_points - self.damage)

    def __str__(self) -> str:
        return f"{super().__str__()} - Tipo: Dano, Dano: {self.damage}"


class HealAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, effect_value: int, description, level=0):
        super().__init__(name, cooldown, level, description)
        self.type = SkillTypeEnum.HEAL
        self.effect_value = effect_value

    def apply(self, caster, _):
        caster.health_points = min(caster.max_hp, caster.health_points + self.effect_value)

    def __str__(self) -> str:
        return f"{super().__str__()} - Tipo: Cura, Cura: {self.effect_value}"


class BuffAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, effect_value: int, description, level=0, buff_type="attack"):
        super().__init__(name, cooldown, level, description)
        self.type = SkillTypeEnum.BUFF
        self.effect_value = effect_value
        self.buff_type = buff_type  # Can be 'attack', 'defense', or 'both'

    def apply(self, caster, _):
        if self.buff_type == "attack":
            caster.attack_points += self.effect_value
        elif self.buff_type == "defense":
            caster.defense_points += self.effect_value
        elif self.buff_type == "both":
            caster.attack_points += self.effect_value
            caster.defense_points += self.effect_value

    def __str__(self) -> str:
        return f"{super().__str__()} - Tipo: Buff, Aumento de Status: {self.effect_value}, Tipo de Buff: {self.buff_type}"


class DebuffAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, effect_value: int, description, level=0, debuff_type="attack"):
        super().__init__(name, cooldown, level, description)
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

    def __str__(self) -> str:
        return f"{super().__str__()} - Tipo: Debuff, Redução de Status: {self.effect_value}, Tipo de Debuff: {self.debuff_type}"


class UtilityAbility(BaseAbility):
    def __init__(self, name: str, cooldown: int, description,  effect_value: int = 0, level=0):
        super().__init__(name, cooldown, level, description)
        self.type = SkillTypeEnum.UTILITY
        self.effect_value = effect_value

    def apply(self, caster, target=None):
        """
        Aplica a habilidade no caster ou no alvo.
        
        Args:
            caster: O personagem que utiliza a habilidade.
            target: O alvo da habilidade, se aplicável.
        """
        raise NotImplementedError("Subclasses devem implementar o método 'apply'.")

    def __str__(self) -> str:
        return f"{super().__str__()} - Tipo: Utility, Efeito: {self.effect_value}"
