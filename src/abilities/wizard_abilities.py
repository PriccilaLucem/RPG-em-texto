from models.abilities_model import HealAbility, UtilityAbility, BuffAbility, DamageAbility, DebuffAbility

class MagicMissile(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Magic Missile",
            cooldown=1,
            damage=15
        )


class Fireball(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Fireball",
            cooldown=3,
            damage=40
        )


class ArcaneBarrier(BuffAbility):
    def __init__(self):
        super().__init__(
            name="Arcane Barrier",
            cooldown=4,
            effect_value=10,  
            buff_type="defense"
        )


class HealWounds(HealAbility):
    def __init__(self):
        super().__init__(
            name="Heal Wounds",
            cooldown=3,
            effect_value=20  
        )


class ManaBurst(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Mana Burst",
            cooldown=5,
            effect_value=10 
        )


class Polymorph(DebuffAbility):
    def __init__(self):
        super().__init__(
            name="Polymorph",
            cooldown=6,
            effect_value=0, 
            debuff_type="attack"
        )
