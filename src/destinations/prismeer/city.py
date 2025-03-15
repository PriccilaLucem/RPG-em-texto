from destinations.prismeer.comercial_center import Comercial_center 
from destinations.prismeer.inn import Inn
from destinations.prismeer.billboard import Billboard

class City():
    
    def __init__(self) -> None:
        self.downtown: Comercial_center = Comercial_center()
        self.billboard: Billboard = Billboard()
        self.inn: Inn = Inn(20, "The Wandering Willow")

    def to_dict(self) -> dict:
        return {
            "downtown": self.downtown.to_dict() if hasattr(self.downtown, "to_dict") else None,
            "billboard": self.billboard.to_dict() if hasattr(self.billboard, "to_dict") else None,
            "inn": self.inn.to_dict() if hasattr(self.inn, "to_dict") else None
        }


    @classmethod
    def from_dict(cls, data: dict):
        city = cls()
        city.downtown = Comercial_center.from_dict(data["downtown"])
        city.billboard = Billboard.from_dict(data["billboard"])
        city.inn = Inn.from_dict(data["inn"])
        return city