from classes.cleric import Cleric
from classes.wizard import Wizard
from classes.warrior import Warrior
from classes.paladin import Paladin
from classes.rogue import Rogue
def get_character_class(class_name: str):
    """
    Retorna uma instância da classe apropriada com base no nome da classe.
    """
    if class_name == "Fighter":
        return Warrior()
    elif class_name == "Rogue":
        return Rogue()
    elif class_name == "Wizard":
        return Wizard()
    elif class_name == "Cleric":
        return Cleric()
    elif class_name == "Paladin":
        return Paladin()
    else:
        raise ValueError(f"Unknown class name: {class_name}")