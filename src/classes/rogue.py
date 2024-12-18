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
