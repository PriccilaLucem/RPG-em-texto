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
