from models.character_class_model import CharacterClass
from abilities.paladin_abilities import DivineSmite, OathOfDevotion, AuraOfProtection, LayOnHands, ShieldOfFaith
class Paladin(CharacterClass):
    def __init__(self):
        super().__init__(
            name="Paladin",
            health=12,  
            primary_stat="Strength",  
            abilities=[DivineSmite(), OathOfDevotion(), AuraOfProtection(), LayOnHands(), ShieldOfFaith()],
            proficiencies=["Heavy Armor", "Martial Weapons", "Shields"],  
            spell_slots=2, 
        )
        self.smite_damage = 10 
        self.aura_range = 10  
        self.lay_on_hands_pool = 20  
        self.oath_benefits = "Oath of Devotion"  
    