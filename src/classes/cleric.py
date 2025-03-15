from models.character_class_model import CharacterClass
from abilities.cleric_abilities import HealingWord, DivineSmite, TurnUndead, BlessingOfProtection, DivineIntervention

class Cleric(CharacterClass):
    def __init__(self):
        super().__init__(
            name="Cleric",
            health=8,
            primary_stat="Wisdom",
            abilities=[
                HealingWord(),
                DivineIntervention(),
                DivineSmite(),
                TurnUndead(),
                BlessingOfProtection()
            ],
            proficiencies=["Light Armor", "Maces", "Shields"],
            spell_slots=2,
        )
        self.divine_intervention_chance = 0.1
        self.healing_power = 5
        self.turn_undead_radius = 15
        self.domain_bonus = "Life Domain"

    def to_dict(self):
        """Convert the Cleric object to a dictionary."""
        return {
            "name": self.name,
            "health": self.health,
            "primary_stat": self.primary_stat,
            "abilities": [ability.to_dict() for ability in self.abilities],
            "proficiencies": self.proficiencies,
            "spell_slots": self.spell_slots,
            "divine_intervention_chance": self.divine_intervention_chance,
            "healing_power": self.healing_power,
            "turn_undead_radius": self.turn_undead_radius,
            "domain_bonus": self.domain_bonus,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Cleric object from a dictionary."""
        cleric = cls()
        cleric.name = data.get("name", "Cleric")
        cleric.health = data.get("health", 8)
        cleric.primary_stat = data.get("primary_stat", "Wisdom")
        cleric.abilities = [cls._create_ability(ability_data) for ability_data in data.get("abilities", [])]
        cleric.proficiencies = data.get("proficiencies", ["Light Armor", "Maces", "Shields"])
        cleric.spell_slots = data.get("spell_slots", 2)
        cleric.divine_intervention_chance = data.get("divine_intervention_chance", 0.1)
        cleric.healing_power = data.get("healing_power", 5)
        cleric.turn_undead_radius = data.get("turn_undead_radius", 15)
        cleric.domain_bonus = data.get("domain_bonus", "Life Domain")
        return cleric

    @staticmethod
    def _create_ability(ability_data):
        """Helper method to create ability objects from dictionary data."""
        ability_classes = {
            "HealingWord": HealingWord,
            "DivineIntervention": DivineIntervention,
            "DivineSmite": DivineSmite,
            "TurnUndead": TurnUndead,
            "BlessingOfProtection": BlessingOfProtection,
        }
        ability_type = ability_data.get("type")
        if ability_type in ability_classes:
            return ability_classes[ability_type]().from_dict(ability_data)
        raise ValueError(f"Unknown ability type: {ability_type}")