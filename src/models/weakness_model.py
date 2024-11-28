class WeaknessModel():
    def __init__(self, name: str, multiplier: float) -> None:
        self.name = name
        self.multiplier = multiplier
    
    def __str__(self):
        return f"Weakness: {self.name} (Multiplier: {self.multiplier}x)"
