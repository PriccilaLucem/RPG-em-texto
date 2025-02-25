from models.abilities_model import HealAbility, UtilityAbility, BuffAbility, DamageAbility, DebuffAbility


class MagicMissile(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Magic Missile",
            cooldown=1,
            damage=15,
            description="A precise and unerring magical projectile that deals consistent damage to an enemy."
        )


class Fireball(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Fireball",
            cooldown=3,
            damage=40,
            description="A devastating explosion of fire that scorches enemies in a large area."
        )


class ArcaneBarrier(BuffAbility):
    def __init__(self):
        super().__init__(
            name="Arcane Barrier",
            cooldown=4,
            effect_value=10,  # Defense increase
            buff_type="defense",
            description="A shimmering barrier of magical energy that fortifies the user's defenses."
        )


class HealWounds(HealAbility):
    def __init__(self):
        super().__init__(
            name="Heal Wounds",
            cooldown=3,
            effect_value=20,  # Heal amount
            description="A restorative spell that mends injuries and revitalizes the target."
        )


class ManaBurst(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Mana Burst",
            cooldown=5,
            effect_value=10,  # Mana restore amount
            description="An explosive surge of arcane power that restores mana to the user or allies."
        )


class Polymorph(DebuffAbility):
    def __init__(self):
        super().__init__(
            name="Polymorph",
            cooldown=6,
            effect_value=0,  # Transformation effect
            debuff_type="attack",
            description="A transformative spell that alters an enemy's form, weakening their attacks."
        )
