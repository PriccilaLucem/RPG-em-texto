from models.npc_model import Character_with_a_quest_model, Character_model
from quests.main_quests import deliver_sword_to_damon
from destinations.nitna_village.nitna_stable import NitnaStable
from typing import Dict, Any

class Nitna():
    def __init__(self):
        self.villagers = [
            Character_model("Larid", speeches=[
                "Hey there, how are you today?",
                "Glad to see you're ok after the accident"
            ]),
            Character_model("Monael", speeches=[
                "You should go to Prismeer, they are hiring adventures",
                "Can't you see I'm busy?"
            ]) 
        ]
        self.mother = Character_with_a_quest_model("Mother", [
            "Please take this sword to Damon in Prismeer. It's urgent - return to me as soon as it's delivered.",
            "You look pale... Here, take this healing potion before you go."
        ], quest=deliver_sword_to_damon)
        self.stable = NitnaStable()

    def return_npc_by_name(self, name):
        for villager in self.villagers + [self.mother]:
            if villager.name == name:
                return villager
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert Nitna instance to a dictionary for serialization."""
        return {
            "villagers": [villager.to_dict() for villager in self.villagers],
            "mother": self.mother.to_dict(),
            "stable": self.stable.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Nitna':
        """Create a Nitna instance from a dictionary."""
        nitna = cls()
        nitna.villagers = [Character_model.from_dict(villager) for villager in data.get("villagers", [])]
        nitna.mother = Character_with_a_quest_model.from_dict(data.get("mother", {}))
        nitna.stable = NitnaStable.from_dict(data.get("stable", {}))
        return nitna