from models.character_class_model import CharacterClass
from abilities.rogue_abilities import DisarmTrap, Evasion, SneakAttack, UncannyDodge

class Rogue(CharacterClass):
    def __init__(self):
        super().__init__(
            name="Rogue",
            health=5,
            primary_stat="Dexterity",
            abilities=[
                DisarmTrap(),
                Evasion(),
                SneakAttack(),
                UncannyDodge(),
            ],
            proficiencies=["Light Armor", "Daggers", "Shortswords", "Thieves' Tools"],
            spell_slots=0,
        )
        self.stealth_level = 5
        self.critical_chance = 0.25
        self.trap_disarm = True
        self.escape_artistry = True

    def to_dict(self):
        """Convert the Rogue object to a dictionary."""
        return {
            "name": self.name,
            "health": self.health,
            "primary_stat": self.primary_stat,
            "abilities": [ability.to_dict() for ability in self.abilities],
            "proficiencies": self.proficiencies,
            "spell_slots": self.spell_slots,
            "stealth_level": self.stealth_level,
            "critical_chance": self.critical_chance,
            "trap_disarm": self.trap_disarm,
            "escape_artistry": self.escape_artistry,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Rogue object from a dictionary."""
        rogue = cls()
        rogue.name = data.get("name", "Rogue")
        rogue.health = data.get("health", 5)
        rogue.primary_stat = data.get("primary_stat", "Dexterity")
        rogue.abilities = [cls._create_ability(ability_data) for ability_data in data.get("abilities", [])]
        rogue.proficiencies = data.get("proficiencies", ["Light Armor", "Daggers", "Shortswords", "Thieves' Tools"])
        rogue.spell_slots = data.get("spell_slots", 0)
        rogue.stealth_level = data.get("stealth_level", 5)
        rogue.critical_chance = data.get("critical_chance", 0.25)
        rogue.trap_disarm = data.get("trap_disarm", True)
        rogue.escape_artistry = data.get("escape_artistry", True)
        return rogue

    @staticmethod
    def _create_ability(ability_data):
        """Helper method to create ability objects from dictionary data."""
        ability_classes = {
            "DisarmTrap": DisarmTrap,
            "Evasion": Evasion,
            "SneakAttack": SneakAttack,
            "UncannyDodge": UncannyDodge,
        }
        ability_type = ability_data.get("type")
        if ability_type in ability_classes:
            return ability_classes[ability_type]().from_dict(ability_data)
        raise ValueError(f"Unknown ability type: {ability_type}")