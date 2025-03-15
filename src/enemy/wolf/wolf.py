from models.enemy_model import EnemyModel
from enums.enemy_type_enum import EnemyTypeEnum
from enums.weakness_enum import WeaknessEnum
from enemy.wolf.drops import sharp_fang, wolf_pelt

wolf = EnemyModel(
    name="Wolf",
    type=EnemyTypeEnum.BEAST,
    attack_points=30,
    defense_points=15,
    attack_multiplier=1.1,
    critical_hit_chance=0.2,
    resistance_factor=0.9,
    health_points=100,
    speed=35,
    weakness=[WeaknessEnum.FIRE],
    immunities=[],
    abilities=[],
    exp_points=50,
    drops=[
        sharp_fang, wolf_pelt
    ],
    location="Dark Woods",
    level=2
)