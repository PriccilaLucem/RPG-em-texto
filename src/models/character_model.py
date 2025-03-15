class Character_model:
    def __init__(self, name: str, speeches: list) -> None:
        self.name = name
        self.speeches = speeches    

    def speech(self, list_index: int) -> str:
        return self.speeches[list_index]

    @classmethod
    def from_dict(cls, data: dict) -> None:
        npc = cls(name=data["name"], speeches=data["speeches"])
        return npc
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "speeches": self.speeches
        }
