from abc import ABC

class CharacterClass(ABC):
    def __init__(self, name, primary_stat, abilities, health, proficiencies, spell_slots):
        self.name = name
        self.primary_stat = primary_stat  
        self.abilities = abilities  
        self.constitution = 10
        self.health = health
        self.proficiencies = proficiencies
        self.spell_slots = spell_slots

    def to_dict(self):
        return {
            "name": self.name,
            "primary_stat": self.primary_stat,
            "abilities": self.abilities,
            "constitution": self.constitution,
            "health": self.health,
            "proficiencies": self.proficiencies,
            "spell_slots": self.spell_slots
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["primary_stat"],
            data["abilities"],
            data["health"],
            data["proficiencies"],
            data["spell_slots"]
        )
