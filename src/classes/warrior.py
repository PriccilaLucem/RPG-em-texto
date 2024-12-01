from models.character_class_model import CharacterClass
class Warrior(CharacterClass):
    def __init__(self):
        super().__init__(
            name="Fighter",
            health=10,
            primary_stat="Strength",  
            abilities=["Second Wind", "Action Surge", "Indomitable"],
            proficiencies=["Heavy Armor", "Shields", "Swords", "Axes", "Melee Weapons"],
            spell_slots=0  
        )
        self.armor_mastery = True
        self.weapon_specialization = ["Swords", "Axes"]
        self.battle_stance = "Balanced"
        self.action_points = 2
