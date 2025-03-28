from destinations.prismeer.inn import Inn
from destinations.prismeer.bar import PrismeerBar
from destinations.prismeer.billboard import Billboard
from characters.damon import Damon
import curses  

class City():
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        self.inn: Inn = Inn(50, "The Wandering Willow")
        self.bar = PrismeerBar(stdscr)
        self.damon = Damon(stdscr)
        self.billboard = Billboard(stdscr)
    
    def to_dict(self) -> dict:
        """Serialize City to dictionary"""
        return {
            "inn": self.inn.to_dict(),
            "bar": self.bar.to_dict(),
            "billboard": self.billboard.to_dict(),
            "damon": self.damon.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict, stdscr: curses.window) -> 'City':
        city = cls(stdscr) 
        city.inn = Inn.from_dict(data["inn"])
        city.bar = PrismeerBar.from_dict(data["bar"], stdscr)
        city.billboard = Billboard.from_dict(data["billboard"], stdscr)
        city.damon = Damon.from_dict(data["damon"], stdscr)
        
        
        return city