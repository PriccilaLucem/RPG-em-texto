from models.abilities_model import HealAbility, UtilityAbility, BuffAbility, DamageAbility, DebuffAbility



class SecondWind(HealAbility):
    def __init__(self):
        super().__init__(
            name="Second Wind",
            cooldown=3,
            effect_value=10  
        )


class ActionSurge(UtilityAbility):
    def __init__(self):
        super().__init__(
            name="Action Surge",
            cooldown=4,
            effect_value=1  
        )

    def apply(self, caster, target=None):
        caster.extra_actions += self.effect_value
        return f"{caster.name} usa {self.name}, ganhando {self.effect_value} ação extra!"



class Indomitable(BuffAbility):
    def __init__(self):
        super().__init__(
            name="Indomitable",
            cooldown=5,
            effect_value=5,  
            buff_type="defense"
        )
