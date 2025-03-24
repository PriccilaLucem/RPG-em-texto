from models.npc_model import Character_with_a_quest_model, Character_model
from quests.main_quests import deliver_sword_to_damon
from destinations.nitna_village.nitna_stable import NitnaStable
from typing import TYPE_CHECKING, Dict, Any
if TYPE_CHECKING:
    from characters.main_character import MainCharacter

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
            "I need you to deliver this to Damon in Prismeer. Come back here as soon as you deliver it",
            "Are you ok? Here take this...",
        ], quest=deliver_sword_to_damon)
        self.stable = NitnaStable()

    def talk_to_npc(self, name, main_character: 'MainCharacter'):
        for npc in self.villagers + [self.mother]:
            if name == "Larid":
                if any(quest.id == -2 for quest in (main_character.concluded_quests or [])):
                    return f"{npc.name}: {npc.speeches[1]}"
                else:
                    return f"{npc.name}: {npc.speeches[0]}"
            elif name == "Monael":
                return f"{npc.name}: {npc.speeches[0]}"
            elif name == "Mother":
                if deliver_sword_to_damon.id in (main_character.quests or []):
                    return f"{npc.name}: {npc.speeches[1]}"
                elif deliver_sword_to_damon.id in (main_character.concluded_quests or []):
                    return f"{npc.name}: Are you okay? What happened to you?"
    
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