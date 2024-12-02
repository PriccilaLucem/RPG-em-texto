from models.abilities_model import DamageAbility, UtilityAbility


class SneakAttack(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Sneak Attack",
            cooldown=1,
            damage=25  # Damage value
        )


class Evasion(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Evasion",
            cooldown=3,
            effect_value=0
        )

    def apply(self, caster, target=None):
        caster.dodge_chance += 50 
        return f"{caster.name} usa {self.name}, aumentando drasticamente sua esquiva!"



class UncannyDodge(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Uncanny Dodge",
            cooldown=2,
            effect_value=0
        )

    def apply(self, caster, target=None):
        if target and hasattr(target, 'last_attack_damage'):
            reduced_damage = target.last_attack_damage // 2
            target.last_attack_damage -= reduced_damage
            return f"{caster.name} usa {self.name}, reduzindo o dano recebido pela metade!"
        return f"{self.name} falhou, pois não havia um ataque recente."


class DisarmTrap(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Disarm Trap",
            cooldown=2,
            effect_value=0
        )

    def apply(self, caster, target=None):
        if target and hasattr(target, 'trap'):
            target.trap.disarmed = True
            return f"{caster.name} usa {self.name} para desarmar uma armadilha!"
        return f"{self.name} falhou, pois nenhuma armadilha foi encontrada."
