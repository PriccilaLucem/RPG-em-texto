from models.abilities_model import DamageAbility

class CrushingHug(DamageAbility):
    def __init__(self, level: int) -> None:
        super().__init__(
            name="Crushing Hug",
            cooldown=5,
            damage=  30 + (level * 0.5),
            description="A powerful ability that deals crushing damage to the target."
        )
