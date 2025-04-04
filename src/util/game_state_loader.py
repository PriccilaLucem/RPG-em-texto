from characters.main_character import MainCharacter
from destinations.prismeer.city import City
from destinations.prismeer.comercial_center import Comercial_center
from destinations.cave.owl_bear_cave import OwlBearCave
from destinations.nitna_village.nitna import Nitna
class GameStateLoader:
    CLASS_MAPPING = {
        'main_character': MainCharacter,
        'prismeer': City,
        'prismeer_downtown': Comercial_center,
        'nitna_village': Nitna,
        'cave': OwlBearCave,
        'forest': None,  # Add Forest class if needed
        'billboard': None  # Add Billboard class if needed
    }

    @classmethod
    def load(cls, raw_data, stdscr=None):
        game_state = {}
        
        for key, value in raw_data.items():
            if value is None:
                game_state[key] = None
                continue
            
            # Preserve boolean values
            if isinstance(value, bool):
                game_state[key] = value
                continue
            
            # Handle special cases (like City needing stdscr)
            if key == 'prismeer' and stdscr is not None:
                game_state[key] = City.from_dict(value, stdscr)
                continue
            
            # Get the appropriate class for this key
            class_type = cls.CLASS_MAPPING.get(key)
            
            if class_type and hasattr(class_type, 'from_dict'):
                game_state[key] = class_type.from_dict(value)
            else:
                game_state[key] = value
        return game_state