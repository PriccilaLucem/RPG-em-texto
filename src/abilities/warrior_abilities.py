from models.abilities_model import HealAbility, UtilityAbility, BuffAbility, DamageAbility, DebuffAbility


class SecondWind(HealAbility):
    def __init__(self):
        super().__init__(
            name="Second Wind",
            cooldown=3,
            effect_value=10,
            description="A surge of resilience that restores a portion of the user's health, keeping them in the fight."
        )
    def to_dict(self):
        return super().to_dict()
    @classmethod
    def from_dict(cls, data):
        return super().from_dict(data)
class ActionSurge(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Action Surge",
            cooldown=4,
            effect_value=1,
            description="A burst of adrenaline that grants the user an additional action during their turn."
        )
    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        return super().from_dict(data)

class Indomitable(BuffAbility):
    def __init__(self):
        super().__init__(
            name="Indomitable",
            cooldown=5,
            effect_value=5,
            buff_type="defense",
            description="An unyielding spirit that bolsters the user's defenses, making them harder to bring down."
        )

    def to_dict(self):
        return super().to_dict()
    @classmethod
    def from_dict(cls, data):
        return super().from_dict(data)