from models.enemy_model import EnemyModel
from enums.weakness_enum import WeaknessEnum
from enums.immunity_enum import ImmunityEnum
from enums.enemy_type_enum import EnemyTypeEnum
from enemy.owl_bear.abilities import CrushingHug
from enemy.owl_bear.drops import sharp_claws, owl_bear_pelt

owl_bear = EnemyModel(name="Owlbear",
                    type=EnemyTypeEnum.BEAST,
                    attack_points=40,
                    defense_points=30,
                    attack_multiplier=1.0,
                    critical_hit_chance=0.05,
                    resistance_factor=1.0,
                    health_points=150,
                    speed=15,
                    weakness=[WeaknessEnum.FIRE.value, WeaknessEnum.SILVER_WEAPONS.value],
                    immunities=[ImmunityEnum.POISON.value, ImmunityEnum.NON_MAGICAL_WEAPONS.value],
                    exp_points=250,
                    drops=[sharp_claws, owl_bear_pelt],
                    location="forest/cave",
                    level = 10, 
                    abilities= [CrushingHug(level=10)]
)