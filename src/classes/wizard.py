from models.character_class_model import CharacterClass
from abilities.wizard_abilities import MagicMissile, Fireball, ArcaneBarrier, HealWounds, ManaBurst, Polymorph

class Wizard(CharacterClass):
    def __init__(self):
        super().__init__(
            name="Wizard",
            health=5,
            primary_stat="Intelligence",
            abilities=[
                MagicMissile(),
                Fireball(),
                ArcaneBarrier(),
                HealWounds(),
                ManaBurst(),
                Polymorph(),
            ],
            proficiencies=["Light Armor", "Daggers", "Wands", "Spellbooks"],
            spell_slots=3,
        )
        self.spell_power = 10
        self.arcane_focus = True
        self.spell_mastery = "Magic Missile"
        self.mana_regeneration = 1
        self.mana = 30

    def to_dict(self):
        """Convert the Wizard object to a dictionary."""
        return {
            "name": self.name,
            "health": self.health,
            "primary_stat": self.primary_stat,
            "abilities": [ability.to_dict() for ability in self.abilities],
            "proficiencies": self.proficiencies,
            "spell_slots": self.spell_slots,
            "spell_power": self.spell_power,
            "arcane_focus": self.arcane_focus,
            "spell_mastery": self.spell_mastery,
            "mana_regeneration": self.mana_regeneration,
            "mana": self.mana,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Wizard object from a dictionary."""
        wizard = cls()
        wizard.name = data.get("name", "Wizard")
        wizard.health = data.get("health", 5)
        wizard.primary_stat = data.get("primary_stat", "Intelligence")
        wizard.abilities = [cls._create_ability(ability_data) for ability_data in data.get("abilities", [])]
        wizard.proficiencies = data.get("proficiencies", ["Light Armor", "Daggers", "Wands", "Spellbooks"])
        wizard.spell_slots = data.get("spell_slots", 3)
        wizard.spell_power = data.get("spell_power", 10)
        wizard.arcane_focus = data.get("arcane_focus", True)
        wizard.spell_mastery = data.get("spell_mastery", "Magic Missile")
        wizard.mana_regeneration = data.get("mana_regeneration", 1)
        wizard.mana = data.get("mana", 30)
        return wizard

    @staticmethod
    def _create_ability(ability_data):
        """Helper method to create ability objects from dictionary data."""
        ability_classes = {
            "MagicMissile": MagicMissile,
            "Fireball": Fireball,
            "ArcaneBarrier": ArcaneBarrier,
            "HealWounds": HealWounds,
            "ManaBurst": ManaBurst,
            "Polymorph": Polymorph,
        }
        ability_type = ability_data.get("type")
        if ability_type in ability_classes:
            return ability_classes[ability_type]().from_dict(ability_data)
        raise ValueError(f"Unknown ability type: {ability_type}")