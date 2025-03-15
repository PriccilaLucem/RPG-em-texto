from models.enemy_model import EnemyModel
from enums.weakness_enum import WeaknessEnum
from enums.enemy_type_enum import EnemyTypeEnum
from enemy.giant_spider.drops import venom_gland, spider_silk 

giant_spider = EnemyModel(
    name="Giant Spider",
    type=EnemyTypeEnum.BEAST,
    attack_points=35,
    defense_points=20,
    attack_multiplier=1.3,
    critical_hit_chance=0.25,
    resistance_factor=1.0,
    health_points=120,
    speed=40,
    weakness=[WeaknessEnum.FIRE],
    immunities=[WeaknessEnum.POISON],
    abilities=[],
    exp_points=60,
    drops=[
        spider_silk, venom_gland
    ],
    location="Spider Nest",
    level=3
)