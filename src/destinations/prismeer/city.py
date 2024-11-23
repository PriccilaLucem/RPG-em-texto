from destinations.prismeer.comercial_center import Comercial_center 
from destinations.prismeer.inn import Inn
from destinations.prismeer.billboard import Billboard
class City():
    
    def __init__(self) -> None:
        self.downtown:Comercial_center = Comercial_center()
        self.billboard: Billboard = Billboard()
        self.inn:Inn = Inn(20)    