from models.abilities_model import (
    HealAbility,
    DamageAbility,
    DebuffAbility,
    BuffAbility,
    UtilityAbility,
)

class HealingWord(HealAbility):
    def __init__(self):
        super().__init__(
            name="Healing Word",
            cooldown=1,
            effect_value=15,
            description="A soothing word that restores health to an ally."
        )


class DivineSmite(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Divine Smite",
            cooldown=3,
            damage=25,
            description="A radiant strike that delivers holy damage to a foe."
        )


class TurnUndead(DebuffAbility):
    def __init__(self):
        super().__init__(
            name="Turn Undead",
            cooldown=5,
            effect_value=10,
            debuff_type="attack",
            description="A holy chant that weakens undead creatures, reducing their attack power."
        )


class BlessingOfProtection(BuffAbility):
    def __init__(self):
        super().__init__(
            name="Blessing of Protection",
            cooldown=4,
            effect_value=10,
            buff_type="defense",
            description="A divine blessing that enhances an ally's defense for a short time."
        )


class DivineIntervention(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Divine Intervention",
            cooldown=10,
            effect_value=0,
            description="A miraculous ability that calls upon divine aid to change the tide of battle."
        )
