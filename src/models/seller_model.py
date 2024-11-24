from items.armor_model import ArmorModel
from items.weapon_model import Weapon_model
from characters.hero import Hero
from models.character_model import Character_model
from typing import List, Union

class Seller_model(Character_model):
    
    def __init__(self, name: str, speeches: list, backpack: List[Union[ArmorModel, Weapon_model]]) -> None:
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
