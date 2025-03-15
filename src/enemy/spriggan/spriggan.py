from enums.enemy_type_enum import EnemyTypeEnum
from enums.weakness_enum import WeaknessEnum
from enums.immunity_enum import ImmunityEnum
from models.enemy_model import EnemyModel
from enemy.spriggan.drops import ancient_bark, forest_gem, mystical_leaf
from enemy.spriggan.abilities import natures_wrath, healing_aura

spriggan = EnemyModel(
    name="Spriggan",
    type=EnemyTypeEnum.MAGICAL,
    attack_points=25,
    defense_points=20,
    attack_multiplier=1.2,
    critical_hit_chance=0.1,
    resistance_factor=0.8,
    health_points=60,
    speed=15,
    weakness=[WeaknessEnum.FIRE],
    immunities=[ImmunityEnum.POISON, ImmunityEnum.PARALYSIS],
    abilities=[
        natures_wrath, healing_aura
    ],
    exp_points=10,
    drops=[
        mystical_leaf, ancient_bark, forest_gem
    ],
    location="Forest",
    level=2
)