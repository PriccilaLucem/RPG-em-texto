class character_model():
    def __init__(self, name: str, speeches: list) -> None:
        self.name = name
        self.speeches = speeches    
    
    def speech(self, list_index:int) -> str:
        return self.speeches[list_index]