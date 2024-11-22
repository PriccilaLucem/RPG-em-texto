from characters.hero import hero
from models.character_model import character_model

class seller_model(character_model):
    
    def __init__(self, name: str, speeches: list, backpack: list) -> None:
        super().__init__(name, speeches)
        self.backpack = backpack
    
    
    def sell_item(self, item_id:int, hero:hero) -> None:
        for item in self.backpack:
            if(item.item_id == item_id):
                if(hero.gold > item.cost):
                    hero.backpack.append(item)
                    self.backpack.remove(item)
                    hero.gold -= item.cost
                    return 
        print("You don't have the necessary gold")