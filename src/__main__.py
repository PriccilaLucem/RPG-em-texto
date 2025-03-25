import curses
from destinations.prismeer.city import City
from characters.main_character import MainCharacter
from global_state.global_state import should_exit, update_game_state, get_game_state
from destinations.cave.owl_bear_cave import OwlBearCave
from destinations.nitna_village.nitna import Nitna
from destinations.nitna_village import NitnaMenu
from menu.menu import Menu
from destinations.crossroads import CrossRoads


def key_pressed_event(stdscr: curses.window, main_character: MainCharacter, prismeer: City, owl_bear_cave: OwlBearCave, nitna: Nitna, menu: Menu):
    update_game_state(is_in_game=True)  # Atualiza o estado global
    nitna_village = NitnaMenu(nitna, stdscr, main_character, menu)
    crossroads = CrossRoads(main_character, prismeer, nitna, stdscr, menu)
    
    while True:
        atual_location = get_game_state().get("atual_location")
        if atual_location in ["nitna_village"]:
            nitna_village.run()
        else:
            crossroads.run()

def game_loop(stdscr: curses.window, main_character: MainCharacter, prismeer: City, owl_bear_cave: OwlBearCave, nitna: Nitna):
    """Main game loop."""
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    menu = Menu(stdscr, main_character, False)
    menu.run()

    game_state = get_game_state()
    atual_location = "nitna_village" if get_game_state().get("atual_location") is None else get_game_state().get("atual_location")
    
    main_character = game_state.get("main_character") if game_state.get("main_character") is not None else main_character
    prismeer = game_state.get("prismeer") if game_state.get("prismeer") is not None else prismeer
    owl_bear_cave = game_state.get("cave") if game_state.get("cave") is not None else owl_bear_cave
    nitna = game_state.get("nitna_village") if game_state.get("nitna_village") is not None else nitna

    update_game_state(main_character=main_character, prismeer=prismeer, cave=owl_bear_cave, nitna_village=nitna, atual_location = atual_location)
    
    while not should_exit():
        key_pressed_event(stdscr, main_character, prismeer, owl_bear_cave, nitna, menu)

def main(stdscr):
    """Initializes the game and starts the main loop."""
    main_character = MainCharacter()
    prismeer = City()
    owl_bear_cave = OwlBearCave()
    nitna = Nitna()
    

    try:
        game_loop(stdscr, main_character, prismeer, owl_bear_cave, nitna)
    except KeyboardInterrupt:
        print("Game interrupted.")
    finally:
        print("Goodbye!")

if __name__ == "__main__":
    curses.wrapper(main)
