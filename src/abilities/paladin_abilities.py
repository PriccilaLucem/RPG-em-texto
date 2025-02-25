from models.abilities_model import HealAbility, DamageAbility, BuffAbility, UtilityAbility


class LayOnHands(HealAbility):
    def __init__(self):
        super().__init__(
            name="Lay on Hands",
            cooldown=2,
            effect_value=20,  # Heal amount
            description="A healing touch that restores health to an ally, mending wounds with divine power."
        )


class DivineSmite(DamageAbility):
    def __init__(self):
        super().__init__(
            name="Divine Smite",
            cooldown=3,
            damage=30,  # Damage amount
            description="A powerful strike imbued with divine energy, dealing radiant damage to an enemy."
        )


class ShieldOfFaith(BuffAbility):
    def __init__(self):
        super().__init__(
            name="Shield of Faith",
            cooldown=5,
            effect_value=10,
            buff_type="defense",
            description="A shimmering shield of divine energy that bolsters an ally's defenses."
        )


class AuraOfProtection(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Aura of Protection",
            cooldown=6,
            effect_value=0,
            description="An aura that extends divine protection to nearby allies, enhancing their resilience."
        )


class OathOfDevotion(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Oath of Devotion",
            cooldown=10,
            effect_value=0,
            description="A solemn vow that empowers allies with unwavering faith and devotion."
        )
