from enums.proeficiency_enum import Proficiency_Enum

class ArmorProficiency:
    def __init__(self):
        self.proficiencies = [Proficiency_Enum.LIGHT_ARMOR, Proficiency_Enum.HEAVY_ARMOR]

    def __str__(self):
        return f"Armor Proficiencies: {', '.join([p.value for p in self.proficiencies])}"

class WeaponProficiency:
    def __init__(self):
        self.proficiencies = [Proficiency_Enum.MARTIAL_WEAPONS, Proficiency_Enum.MACES, 
                              Proficiency_Enum.SWORDS, Proficiency_Enum.AXES, 
                              Proficiency_Enum.DAGGERS, Proficiency_Enum.SHORTSWORDS]

    def __str__(self):
        return f"Weapon Proficiencies: {', '.join([p.value for p in self.proficiencies])}"

class ShieldProficiency:
    def __init__(self):
        self.proficiencies = [Proficiency_Enum.SHIELDS]

    def __str__(self):
        return f"Shield Proficiencies: {', '.join([p.value for p in self.proficiencies])}"

class ThiefProficiency:
    def __init__(self):
        self.proficiencies = [Proficiency_Enum.DAGGERS, Proficiency_Enum.THIEVES_TOOLS]

    def __str__(self):
        return f"Thief Proficiencies: {', '.join([p.value for p in self.proficiencies])}"

class SpellcasterProficiency:
    def __init__(self):
        self.proficiencies = [Proficiency_Enum.WANDS, Proficiency_Enum.SPELLBOOKS]

    def __str__(self):
        return f"Spellcaster Proficiencies: {', '.join([p.value for p in self.proficiencies])}"
