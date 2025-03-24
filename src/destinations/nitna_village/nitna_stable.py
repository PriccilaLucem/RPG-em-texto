from models.horse_model import Horse
from models.stable_model import Stable
from models.npc_model import Character_model

class NitnaStable(Stable):
    def __init__(self):
        horses = [
            Horse("Thunder", "Arabian", speed=8, stamina=7, price=200),
            Horse("Shadowfax", "Mearas", speed=10, stamina=9, price=250),  
            Horse("Bucephalus", "Thessalian", speed=9, stamina=6, price=225),  
            Horse("Roach", "Percheron", speed=6, stamina=8, price= 180) 
        ]
        
        owner = Character_model("Nitz", [
            "Hello want to buy a horse?",
            "What are you staring at, that's my horse!"
        ])
        super().__init__(horses, owner)

    def to_dict(self) -> dict:
        return {
            "horses": [horse.to_dict() for horse in self.horses],
            "owner": self.owner.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'NitnaStable':
        stable = cls()
        stable.horses = [Horse.from_dict(horse_data) for horse_data in data.get("horses", [])]
        stable.owner = Character_model.from_dict(data.get("owner", {}))
        return stable