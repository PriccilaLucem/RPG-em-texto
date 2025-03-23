class Horse:
    def __init__(self, name: str, breed: str, speed: int, stamina: int):
        self.name = name
        self.breed = breed
        self.speed = speed
        self.stamina = stamina

    def __str__(self):
        return f"{self.name} ({self.breed}) - Speed: {self.speed}, Stamina: {self.stamina}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "breed": self.breed,
            "speed": self.speed,
            "stamina": self.stamina
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Horse":
        return cls(
            name=data["name"],
            breed=data["breed"],
            speed=data["speed"],
            stamina=data["stamina"]
        )
