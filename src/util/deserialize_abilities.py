from enums.skill_type_enum import SkillTypeEnum
from models.abilities_model import DamageAbility, HealAbility, BuffAbility, DebuffAbility, UtilityAbility
def deserialize_ability(data: dict):
    """
    Deserializa uma habilidade a partir de um dicionário de dados.

    Args:
        data (dict): Dicionário contendo os dados da habilidade.

    Returns:
        BaseAbility: Instância da habilidade deserializada.
    """
    skill_type = SkillTypeEnum[data["type"]]  # Converte o tipo de habilidade para o enum correspondente

    if skill_type == SkillTypeEnum.DAMAGE:
        return DamageAbility.from_dict(data)
    elif skill_type == SkillTypeEnum.HEAL:
        return HealAbility.from_dict(data)
    elif skill_type == SkillTypeEnum.BUFF:
        return BuffAbility.from_dict(data)
    elif skill_type == SkillTypeEnum.DEBUFF:
        return DebuffAbility.from_dict(data)
    elif skill_type == SkillTypeEnum.UTILITY:
        return UtilityAbility.from_dict(data)
    else:
        raise ValueError(f"Tipo de habilidade desconhecido: {data['type']}")