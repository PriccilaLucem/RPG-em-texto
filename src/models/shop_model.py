from models.seller_model import Seller_model
from characters.hero import Hero

class Shop_model():
        def __init__(self, name: str, seller_name:str, speeches: list, backpack: list) -> None:
                self.seller = Seller_model(seller_name, speeches, backpack)
                self.name = name
        

        def shop_interactions(self, main_character:Hero):
                print(f"""
                            You entered the {self.name} shop, what would you like to do?
                            T - Talk to the seller
                            B - Buy itens
                            E - Leave the armor shop
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
                                        self.seller.show_inventary()

                                case "E":
                                        print("You are leaving the armor shop...")
                                        break