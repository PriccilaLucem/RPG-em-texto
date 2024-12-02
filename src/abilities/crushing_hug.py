from models.abilities_model import DamageAbility

class CrushingHug(DamageAbility):
    def __init__(self, level: int) -> None:
        base_damage = 30 + (level * 0.5)
        super().__init__(
            name="Crushing Hug",
            cooldown=5,
            damage=base_damage
        )
