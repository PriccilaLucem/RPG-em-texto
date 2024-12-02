from models.abilities_model import HealAbility, DamageAbility, BuffAbility, UtilityAbility


class LayOnHands(HealAbility):
    def __init__(self):
        super().__init__(
            name="Lay on Hands",
            cooldown=2,
            effect_value=20  # Heal amount
        )


class DivineSmite(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Divine Smite",
            cooldown=3,
            damage=30  # Damage amount
        )


class ShieldOfFaith(BuffAbility):
    def __init__(self):
        super().__init__(
            name="Shield of Faith",
            cooldown=5,
            effect_value=10,
            buff_type="defense"
        )


class AuraOfProtection(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Aura of Protection",
            cooldown=6,
            effect_value=0  
        )

class OathOfDevotion(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Oath of Devotion",
            cooldown=10,
            effect_value=0  
        )
