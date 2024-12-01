from models.character_class_model import CharacterClass

class Wizard(CharacterClass):
    def __init__(self):
        super().__init__(
            name="Wizard",
            health=5,
            primary_stat="Intelligence",
            abilities=["Spellcasting", "Arcane Recovery", "Ritual Casting"],
            proficiencies=["Light Armor", "Daggers", "Wands", "Spellbooks"],
            spell_slots=3 
        )
        self.spell_power = 10
        self.arcane_focus = True
        self.spell_mastery = "Magic Missile"
        self.mana_regeneration = 1
