from typing import Any, List, Tuple, Dict, Optional, TYPE_CHECKING
from util.id_generator import IDGenerator

if TYPE_CHECKING:
    from models.item_model import ItemModel
    from characters.main_character import MainCharacter


class Quests:
    def __init__(
        self,
        id: Optional[int] = None,
        difficult_stars: int = 1,
        xp_given: int = 0,
        gold_given: int = 0,
        mission: str = "",
        description: str = "",
        additional_info: Optional[Dict[str, Any]] = None
    ) -> None:
        self.id = id if id is not None else IDGenerator.generate_id()
        self.difficult_stars = difficult_stars
        self.xp_given = xp_given
        self.gold_given = gold_given
        self.mission = mission
        self.description = description
        self.additional_info = additional_info or {}

    def __str__(self) -> str:
        info = [
            f"Mission: {self.mission}",
            f"Difficulty: {'★' * self.difficult_stars}",
            f"Reward: {self.gold_given} gold | {self.xp_given} XP"
        ]
        if self.description:
            info.append(f"\nDescription: {self.description}")
        if self.additional_info:
            info.append("\nAdditional Info:")
            info.extend(f"- {k}: {v}" for k, v in self.additional_info.items())
        return "\n".join(info)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Quests":
        return cls(
            id=data.get("id"),
            difficult_stars=data["difficult_stars"],
            xp_given=data["xp_given"],
            gold_given=data["gold_given"],
            mission=data["mission"],
            description=data.get("description", ""),
            additional_info=data.get("additional_info", {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "difficult_stars": self.difficult_stars,
            "xp_given": self.xp_given,
            "gold_given": self.gold_given,
            "mission": self.mission,
            "description": self.description,
            "additional_info": self.additional_info
        }


class CollectableQuest(Quests):
    def __init__(
        self,
        id: Optional[int] = None,
        difficult_stars: int = 1,
        xp_given: int = 0,
        gold_given: int = 0,
        mission: str = "",
        description: str = "",
        additional_info: Optional[Dict[str, Any]] = None,
        items_to_be_collected: Optional[List[Tuple[Any, int]]] = None
    ) -> None:
        super().__init__(
            id=id,
            difficult_stars=difficult_stars,
            xp_given=xp_given,
            gold_given=gold_given,
            mission=mission,
            description=description,
            additional_info=additional_info
        )
        self.items_to_be_collected = items_to_be_collected or []

    def __str__(self) -> str:
        base_str = super().__str__()
        items_str = "\nItems to collect:\n" + "\n".join(
            f"- {item[0].name if hasattr(item[0], 'name') else item[0]} x{item[1]}"
            for item in self.items_to_be_collected
        )
        return f"{base_str}{items_str}"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CollectableQuest":
        base_quest = super().from_dict(data)
        return cls(
            id=base_quest.id,
            difficult_stars=base_quest.difficult_stars,
            xp_given=base_quest.xp_given,
            gold_given=base_quest.gold_given,
            mission=base_quest.mission,
            description=base_quest.description,
            additional_info=base_quest.additional_info,
            items_to_be_collected=[
                (item_data["item"], item_data["quantity"])
                for item_data in data.get("items_to_be_collected", [])
            ]
        )

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["items_to_be_collected"] = [
            {
                "item": item[0].to_dict() if hasattr(item[0], "to_dict") else item[0],
                "quantity": item[1]
            }
            for item in self.items_to_be_collected
        ]
        return data


class DeliverQuestsItems(Quests):
    def __init__(
        self,
        id: Optional[int] = None,
        difficult_stars: int = 1,
        xp_given: int = 0,
        gold_given: int = 0,
        mission: str = "",
        description: str = "",
        additional_info: Optional[Dict[str, Any]] = None,
        item_to_be_delivered: Optional[Any] = None
    ) -> None:
        super().__init__(
            id=id,
            difficult_stars=difficult_stars,
            xp_given=xp_given,
            gold_given=gold_given,
            mission=mission,
            description=description,
            additional_info=additional_info
        )
        self.item_to_be_delivered = item_to_be_delivered

    def __str__(self) -> str:
        base_str = super().__str__()
        item_str = f"\nItem to deliver: {self.item_to_be_delivered.name if hasattr(self.item_to_be_delivered, 'name') else self.item_to_be_delivered}"
        return f"{base_str}{item_str}"

    def deliver_item(self, character: "MainCharacter") -> bool:
        if self.item_to_be_delivered in character.backpack:
            character.remove_items_from_backpack(self.item_to_be_delivered)
            return True
        return False

    def append_item(self, character: "MainCharacter") -> None:
        character.add_to_inventory(self.item_to_be_delivered)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeliverQuestsItems":
        base_quest = super().from_dict(data)
        return cls(
            id=base_quest.id,
            difficult_stars=base_quest.difficult_stars,
            xp_given=base_quest.xp_given,
            gold_given=base_quest.gold_given,
            mission=base_quest.mission,
            description=base_quest.description,
            additional_info=base_quest.additional_info,
            item_to_be_delivered=data["item_to_be_delivered"]  # Assuming this is already deserialized
        )

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["item_to_be_delivered"] = (
            self.item_to_be_delivered.to_dict()
            if hasattr(self.item_to_be_delivered, "to_dict")
            else self.item_to_be_delivered
        )
        return data