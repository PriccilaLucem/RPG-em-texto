from enums.enemy_type_enum import EnemyType
from enums.weakness_enum import WeaknessEnum
from enums.immunity_enum import ImmunityEnum
from models.enemy_model import EnemyModel
from enemy.treant.drops import ancient_bark, glowing_sap

treant = EnemyModel(
    name="Treant",
    type=EnemyType.ELEMENTAL,
    attack_points=40,
    defense_points=50,
    attack_multiplier=1.0,
    critical_hit_chance=0.05,
    resistance_factor=1.2,
    health_points=200,
    speed=15,
    weakness=[WeaknessEnum.FIRE, WeaknessEnum.LIGHTNING],
    immunities=[ImmunityEnum.WATER],
    abilities=[],
    exp_points=100,
    drops=[
        ancient_bark, glowing_sap
    ],
    location="Deep Forest",
    level=4
)
