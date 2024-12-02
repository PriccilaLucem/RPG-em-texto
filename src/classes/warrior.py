from models.character_class_model import CharacterClass
from abilities.warrior_abilities import SecondWind, ActionSurge,Indomitable

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
