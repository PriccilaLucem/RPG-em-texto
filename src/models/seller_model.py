from characters.hero import Hero
from models.character_model import Character_model

class Seller_model(Character_model):
    
    def __init__(self, name: str, speeches: list, backpack:list) -> None:
        super().__init__(name, speeches)
        self.backpack = backpack
    
    def show_backpack(self):
        return list(map(str, self.backpack))
        
    
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

    @classmethod
    def from_dict(cls, data: dict) -> None:
        name = data.get("name")
        speeches = data.get("speeches", [])
        backpack = data.get("backpack", [])
        seller = cls(name=name, speeches=speeches, backpack=backpack)
        return seller   