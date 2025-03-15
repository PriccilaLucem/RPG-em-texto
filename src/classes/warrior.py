from models.character_class_model import CharacterClass
from abilities.warrior_abilities import SecondWind, ActionSurge, Indomitable

class Warrior(CharacterClass):
    def __init__(self):
        super().__init__(
            name="Fighter",
            health=10,
            primary_stat="Strength",
            abilities=[
                ActionSurge(),
                SecondWind(),
                Indomitable()
            ],
            proficiencies=["Heavy Armor", "Swords", "Axes", "Shields"],
            spell_slots=0
        )
        self.armor_mastery = True
        self.battle_stance = "Balanced"
        self.action_points = 2

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "primary_stat": self.primary_stat,
            "abilities": [ability.to_dict() for ability in self.abilities],
            "proficiencies": self.proficiencies,
            "spell_slots": self.spell_slots,
            "armor_mastery": self.armor_mastery,
            "battle_stance": self.battle_stance,
            "action_points": self.action_points
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.name = data["name"]
        instance.health = data["health"]
        instance.primary_stat = data["primary_stat"]
        instance.abilities = [ability_data.from_dict for ability_data in data["abilities"]]
        instance.proficiencies = data["proficiencies"]
        instance.spell_slots = data["spell_slots"]
        instance.armor_mastery = data["armor_mastery"]
        instance.battle_stance = data["battle_stance"]
        instance.action_points = data["action_points"]
        return instance
    
    @staticmethod
    def _create_ability(ability_data):
        """Helper method to create ability objects from dictionary data."""
        ability_classes = {
            "ActionSurge":ActionSurge, 
            "SecondWind": SecondWind,
            "Indomitable": Indomitable
    
        }
        ability_type = ability_data.get("type")
        if ability_type in ability_classes:
            return ability_classes[ability_type]().from_dict(ability_data)
        raise ValueError(f"Unknown ability type: {ability_type}")