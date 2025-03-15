from characters.hero import Hero
from models.character_model import Character_model
from models.item_model import ItemModel

class Seller_model(Character_model):
    
    def __init__(self, name: str, speeches: list, backpack) -> None:
        super().__init__(name, speeches)
        self.backpack = backpack
    
    def show_backpack(self):
        return "\n".join(map(str, self.backpack))  
        
    
    def sell_item(self, item_id: int, hero: Hero) -> None:
            for item in self.backpack:
                if getattr(item, "item_id", None) == item_id:  
                    if hero.gold >= getattr(item, "cost", 0):  
                        hero.backpack.append(item)  
                        self.backpack.remove(item)  
                        hero.gold -= getattr(item, "cost", 0)  
                        print(f"You successfully bought {item.name}!")
                        return
                    else:
                        print("You don't have the necessary gold.")
                        return
            print("Item not found in the shop.")
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "speeches": self.speeches,
            "backpack": [item.to_dict() if hasattr(item, "to_dict") else str(item) for item in self.backpack]
        } 

    def from_dict(self, data: dict) -> None:
        self.name = data.get("name", "")
        self.speeches = data.get("speeches", [])
        self.backpack = [ItemModel.from_dict(item) if isinstance(item, dict) else item for item in data.get("backpack", [])]
