from models.seller_model import seller_model

class shop_model():
        def __init__(self, name: str, speeches: list, backpack: list) -> None:
                self.seller = seller_model(name, speeches, backpack)                        