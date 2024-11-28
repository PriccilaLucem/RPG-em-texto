from models.enemy_model import Enemy_model
from enums.weakness_enum import WeaknessEnum
from enums.immunity_enum import ImmunityEnum
from enums.enemy_type_enum import EnemyType
from abilities.crushing_hug import CrushingHug

class owl_bear(Enemy_model):
    def __init__(self, 
                  name="Owlbear",
                    type=EnemyType.BEAST,
                    attack_points=20,
                    defense_points=15,
                    attack_multiplier=1.0,
                    critical_hit_chance=0.05,
                    resistance_factor=1.0,
                    health_points=100,
                    speed=15,
                    weakness=[WeaknessEnum.FIRE.value, WeaknessEnum.SILVER_WEAPONS.value],
                    immunities=[ImmunityEnum.POISON.value, ImmunityEnum.NON_MAGICAL_WEAPONS.value],
                    abilities=[CrushingHug],
                    exp_points=250,
                    drops=["owlbear pelt", "sharp claws"],
                    location="forest"
    ) -> None:
        super().__init__(name,
                          type,
                          attack_points, 
                          defense_points, 
                          attack_multiplier, 
                          critical_hit_chance, 
                          resistance_factor, 
                          health_points, 
                          speed, weakness, 
                          immunities, 
                          abilities, 
                          exp_points, 
                          drops, 
                          location)
