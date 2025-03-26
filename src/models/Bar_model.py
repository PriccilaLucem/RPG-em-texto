from typing import List, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from models.item_model import Food
    from models.npc_model import Character_model, Character_with_a_quest_model, Seller_model
    from characters.main_character import MainCharacter

class Bar():
    def __init__(self, food:List[Food], people: List[Union[Character_model, Character_with_a_quest_model]],
            bartender: Seller_model, bardo: Character_model):
        self.food = food
        self.people = people
        self.bartender = bartender
        self.bardo = bardo

    def sell_food(self, id: int, main_character:MainCharacter):
        food_to_sell = next((food for food in self.food if food.item_id == id), None)
        if main_character.gold < food_to_sell.value:
            return "You don't have enought gold"
        main_character.add_to_inventory(food_to_sell)
        main_character.gold -= food_to_sell.value
        return f"You bought {food_to_sell.name} for {food_to_sell.value}"