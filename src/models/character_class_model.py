from abc import ABC

class CharacterClass(ABC):
    def __init__(self, name, primary_stat, abilities, health, proficiencies, spell_slots):
        self.name = name
        self.primary_stat = primary_stat  
        self.abilities = abilities 
        self.consituition = 10
        self.health = health
        self.proficiencies = proficiencies
        self.spell_slots = spell_slots