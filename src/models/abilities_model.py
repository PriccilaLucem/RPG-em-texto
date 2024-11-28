from util.id_generator import IDGenerator
from enums.skill_type_enum import SkillTypeEnum

class Ability_Model():
    def __init__(self, name: str, type: SkillTypeEnum,  cooldown: int,  level = 0, damage: int  = 0, effect_value: int = 0) -> None:
        self.id = IDGenerator.generate_id()
        self.name = name
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.type = type
        self.damage = damage + (level * 0.5)
        self.effect_value = effect_value
        
    def reduce_cooldown(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def is_ready(self) -> bool:

        return self.current_cooldown == 0

    def __str__(self) -> str:
        if self.type == SkillTypeEnum.DAMAGE:
            return f"{self.id}: {self.name} (Tipo: {self.type}), Dano: {self.damage}"
        elif self.type == SkillTypeEnum.HEAL:
            return f"{self.id}: {self.name} (Tipo: {self.type}), Cura: {self.effect_value}"
        elif self.type == SkillTypeEnum.BUFF:
            return f"{self.id}: {self.name} (Tipo: {self.type}), Aumento de Status: {self.effect_value}"
        elif self.type == SkillTypeEnum.DEBUFF:
            return f"{self.id}: {self.name} (Tipo: {self.type}), Redução de Status: {self.effect_value}"
        elif self.type == SkillTypeEnum.UTILITY:
            return f"{self.id}: {self.name} (Tipo: {self.type}), Efeito de utilidade: {self.effect_value}"
        else:
            return f"{self.id}: {self.name} (Tipo: {self.type}), Efeito desconhecido"