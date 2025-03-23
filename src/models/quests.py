from typing import Any, List, Tuple, TYPE_CHECKING
from util.id_generator import IDGenerator

if TYPE_CHECKING:
    from models.item_model import ItemModel
    from characters.main_character import MainCharacter


class Quests:
    def __init__(self, id: int, difficult_stars: int, xp_given: int, gold_given: int, mission: str) -> None:
        self.difficult_stars = difficult_stars
        self.xp_given = xp_given
        self.gold_given = gold_given
        self.mission = mission
        self.id = id if id is not None else IDGenerator.generate_id()

    def __str__(self) -> str:
        return f"Mission: {self.mission} Difficulty: {self.difficult_stars} stars XP: {self.xp_given} Gold: {self.gold_given}"

    @classmethod
    def from_dict(cls, data: dict) -> "Quests":
        return cls(
            id=data["id"],
            difficult_stars=data["difficult_stars"],
            xp_given=data["xp_given"],
            gold_given=data["gold_given"],
            mission=data["mission"]
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "difficult_stars": self.difficult_stars,
            "xp_given": self.xp_given,
            "gold_given": self.gold_given,
            "mission": self.mission
        }

class CollectableQuest(Quests):
    def __init__(self, id: int, difficult_stars: int, xp_given: int, gold_given: int, mission: str, items_to_be_collected: List[Tuple[Any, int]]) -> None:
        super().__init__(id, difficult_stars, xp_given, gold_given, mission)
        self.items_to_be_collected = items_to_be_collected

    def __str__(self) -> str:
        items_str = ", ".join([f"{item} x{quantity}" for item, quantity in self.items_to_be_collected])
        return (f"Mission: {self.mission} Items to collect: {items_str}  "
                f"Difficulty: {self.difficult_stars} stars XP: {self.xp_given} Gold: {self.gold_given}")
    
    @classmethod
    def from_dict(cls, data: dict) -> "CollectableQuest":
        # First, create the base Quests instance
        quest = Quests.from_dict(data)
        # Now, pass the `items_to_be_collected` to the CollectableQuest
        items_to_be_collected = data.get('items_to_be_collected', [])
        return cls(
            id=quest.id,
            difficult_stars=quest.difficult_stars,
            xp_given=quest.xp_given,
            gold_given=quest.gold_given,
            mission=quest.mission,
            items_to_be_collected=items_to_be_collected
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["items_to_be_collected"] = [{"item": item.to_dict() if hasattr(item, "to_dict") else item, "quantity": quantity} 
                                          for item, quantity in self.items_to_be_collected]
        return data
    
class DeliverQuestsItems(Quests):
    def __init__(self, id: int, difficult_stars: int, xp_given: int, gold_given: int, mission: str, item: "ItemModel") -> None:
        super().__init__(id, difficult_stars, xp_given, gold_given, mission)
        self.item = item

    def deliver_item(self, character: "MainCharacter") -> None:
        if self.item in character.backpack:
            character.remove_items_from_backpack(self.item)

    def append_item(self, character: "MainCharacter") -> None:
        character.add_to_inventory(self.item)
