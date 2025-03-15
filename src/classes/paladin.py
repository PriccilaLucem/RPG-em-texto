from models.character_class_model import CharacterClass
from abilities.paladin_abilities import DivineSmite, OathOfDevotion, AuraOfProtection, LayOnHands, ShieldOfFaith

class Paladin(CharacterClass):
    def __init__(self):
        super().__init__(
            name="Paladin",
            health=12,
            primary_stat="Strength",
            abilities=[
                DivineSmite(),
                OathOfDevotion(),
                AuraOfProtection(),
                LayOnHands(),
                ShieldOfFaith()
            ],
            proficiencies=["Heavy Armor", "Martial Weapons", "Shields"],
            spell_slots=2,
        )
        self.smite_damage = 10
        self.aura_range = 10
        self.lay_on_hands_pool = 20
        self.oath_benefits = "Oath of Devotion"

    def to_dict(self):
        """Convert the Paladin object to a dictionary."""
        return {
            "name": self.name,
            "health": self.health,
            "primary_stat": self.primary_stat,
            "abilities": [ability.to_dict() for ability in self.abilities],
            "proficiencies": self.proficiencies,
            "spell_slots": self.spell_slots,
            "smite_damage": self.smite_damage,
            "aura_range": self.aura_range,
            "lay_on_hands_pool": self.lay_on_hands_pool,
            "oath_benefits": self.oath_benefits,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Paladin object from a dictionary."""
        paladin = cls()
        paladin.name = data.get("name", "Paladin")
        paladin.health = data.get("health", 12)
        paladin.primary_stat = data.get("primary_stat", "Strength")
        paladin.abilities = [cls._create_ability(ability_data) for ability_data in data.get("abilities", [])]
        paladin.proficiencies = data.get("proficiencies", ["Heavy Armor", "Martial Weapons", "Shields"])
        paladin.spell_slots = data.get("spell_slots", 2)
        paladin.smite_damage = data.get("smite_damage", 10)
        paladin.aura_range = data.get("aura_range", 10)
        paladin.lay_on_hands_pool = data.get("lay_on_hands_pool", 20)
        paladin.oath_benefits = data.get("oath_benefits", "Oath of Devotion")
        return paladin

    @staticmethod
    def _create_ability(ability_data):
        """Helper method to create ability objects from dictionary data."""
        ability_classes = {
            "DivineSmite": DivineSmite,
            "OathOfDevotion": OathOfDevotion,
            "AuraOfProtection": AuraOfProtection,
            "LayOnHands": LayOnHands,
            "ShieldOfFaith": ShieldOfFaith,
        }
        ability_type = ability_data.get("type")
        if ability_type in ability_classes:
            return ability_classes[ability_type]().from_dict(ability_data)
        raise ValueError(f"Unknown ability type: {ability_type}")
    