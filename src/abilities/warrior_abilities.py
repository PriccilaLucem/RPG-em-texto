from models.abilities_model import HealAbility, UtilityAbility, BuffAbility, DamageAbility, DebuffAbility


class SecondWind(HealAbility):
    def __init__(self):
        super().__init__(
            name="Second Wind",
            cooldown=3,
            effect_value=10,  # Heal amount
            description="A surge of resilience that restores a portion of the user's health, keeping them in the fight."
        )


class ActionSurge(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Action Surge",
            cooldown=4,
            effect_value=1,  # Number of extra actions
            description="A burst of adrenaline that grants the user an additional action during their turn."
        )

    def apply(self, caster, target=None):
        caster.extra_actions += self.effect_value
        return f"{caster.name} uses {self.name}, gaining {self.effect_value} extra action!"


class Indomitable(BuffAbility):
    def __init__(self):
        super().__init__(
            name="Indomitable",
            cooldown=5,
            effect_value=5, 
            buff_type="defense",
            description="An unyielding spirit that bolsters the user's defenses, making them harder to bring down."
        )
