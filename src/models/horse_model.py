from util.id_generator import IDGenerator
class Horse:
    def __init__(self, name: str, breed: str, speed: int, stamina: int, price: int):
        self.id = IDGenerator.generate_id()
        self.name = name
        self.breed = breed
        self.speed = speed
        self.stamina = stamina
        self.price = price
    
    def __str__(self):
        return f"{self.name} ({self.breed}) - Speed: {self.speed}, Stamina: {self.stamina}, Price: {self.price}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "breed": self.breed,
            "speed": self.speed,
            "stamina": self.stamina
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Horse":
        return cls(
            id = data["id"],
            name=data["name"],
            breed=data["breed"],
            speed=data["speed"],
            stamina=data["stamina"]
        )
