from models.seller_model import seller_model
from characters.hero import hero

class shop_model():
        def __init__(self, name: str, seller_name:str, speeches: list, backpack: list) -> None:
                self.seller = seller_model(seller_name, speeches, backpack)
                self.name = name
        

        def shop_interactions(self, main_character:hero):
                print(f"""
                            You entered the {self.name} shop, what would you like to do?
                            T - Talk to the seller
                            B - Buy itens
                            """)
                shop_speech = 0
                while True:
                        shop_key = input().strip().capitalize()
                        match shop_key:
                                case "T":
                                        if(shop_speech < len(self.seller.speeches)):
                                                print(self.seller.speech(shop_speech))
                                                shop_speech += 1
                                        else:
                                                print(self.seller.speech(-1))
                                case "B":
                                        # create an item class 
                                        for item in self.seller.backpack:
                                                print(item.__dict__)
        