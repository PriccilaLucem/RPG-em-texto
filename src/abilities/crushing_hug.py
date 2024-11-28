from enums.skill_type_enum import SkillTypeEnum
from models.abilities_model import Ability_Model

class CrushingHug(Ability_Model):
    def __init__(self, level) -> None:
        super().__init__("Crushing hug", SkillTypeEnum.DAMAGE, 5, 30 + (level* 0.5), 0)

