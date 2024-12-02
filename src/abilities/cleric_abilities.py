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
            effect_value=15  
        )


class DivineSmite(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Divine Smite",
            cooldown=3,
            damage=25 
        )


class TurnUndead(DebuffAbility):
    def __init__(self):
        super().__init__(
            name="Turn Undead",
            cooldown=5,
            effect_value=10,  
            debuff_type="attack"  
        )


class BlessingOfProtection(BuffAbility):
    def __init__(self):
        super().__init__(
            name="Blessing of Protection",
            cooldown=4,
            effect_value=10,  
            buff_type="defense"
        )



class DivineIntervention(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Divine Intervention",
            cooldown=10,
            effect_value=0  
        )
