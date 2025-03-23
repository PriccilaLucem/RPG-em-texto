from destinations.prismeer.comercial_center import Comercial_center 
from destinations.prismeer.inn import Inn

class City():
    
    def __init__(self) -> None:
        self.inn: Inn = Inn(50, "The Wandering Willow")

    def to_dict(self) -> dict:
        return {
            "inn": self.inn.to_dict() if hasattr(self.inn, "to_dict") else None
        }


    @classmethod
    def from_dict(cls, data: dict):
        city = cls()
        city.inn = Inn.from_dict(data["inn"])
        return city