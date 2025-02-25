from models.abilities_model import DamageAbility, UtilityAbility


class SneakAttack(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Sneak Attack",
            cooldown=1,
            damage=25,  # Damage value
            description="A precise and unexpected strike that deals significant damage to an unsuspecting enemy."
        )


class Evasion(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Evasion",
            cooldown=3,
            effect_value=0,
            description="A nimble maneuver that drastically increases the user's dodge chance, avoiding incoming attacks."
        )

    def apply(self, caster, target=None):
        caster.dodge_chance += 50
        return f"{caster.name} uses {self.name}, drastically increasing their dodge chance!"


class UncannyDodge(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Uncanny Dodge",
            cooldown=2,
            effect_value=0,
            description="A reactive ability that halves the damage of the last attack targeting the user."
        )

    def apply(self, caster, target=None):
        if target and hasattr(target, 'last_attack_damage'):
            reduced_damage = target.last_attack_damage // 2
            target.last_attack_damage -= reduced_damage
            return f"{caster.name} uses {self.name}, reducing the damage received by half!"
        return f"{self.name} failed as no recent attack was detected."


class DisarmTrap(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Disarm Trap",
            cooldown=2,
            effect_value=0,
            description="A careful action to disable traps, ensuring the safety of the user and their allies."
        )

    def apply(self, caster, target=None):
        if target and hasattr(target, 'trap'):
            target.trap.disarmed = True
            return f"{caster.name} uses {self.name} to disarm a trap!"
        return f"{self.name} failed as no trap was found."
