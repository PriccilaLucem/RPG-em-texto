from models.enemy_model import EnemyModel
from enums.weakness_enum import WeaknessEnum
from enemy.goblin.drops import goblin_ear, rusty_dagger
from enums.enemy_type_enum import EnemyType

goblin = EnemyModel(
    name="Goblin",
    type=EnemyType.HUMANOID,
    attack_points=20,
    defense_points=10,
    attack_multiplier=1.2,
    critical_hit_chance=0.15,
    resistance_factor=0.8,
    health_points=80,
    speed=25,
    weakness=[WeaknessEnum.FIRE],
    immunities=[],
    abilities=[],
    exp_points=40,
    drops=[
        rusty_dagger, goblin_ear
    ],
    location="Dark Woods",
    level=1
)
