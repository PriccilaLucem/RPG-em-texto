import curses
from destinations.prismeer.city import City
from characters.main_character import MainCharacter
from global_state.global_state import should_exit, update_game_state, get_game_state
from util.display_message import display_message, draw_menu
from destinations.cave.owl_bear_cave import OwlBearCave
from destinations.nitna_village.nitna import Nitna
from destinations.nitna_village import NitnaVillage
from menu.menu import Menu
from destinations.crossroads.Crossroads import Crossroads

def key_pressed_event(stdscr: curses.window, main_character: MainCharacter, prismeer: City, owl_bear_cave: OwlBearCave, nitna: Nitna, atual_location: str, menu: Menu):
    update_game_state(is_in_game=True)  # Atualiza o estado global

    nitna_village = NitnaVillage(nitna, stdscr, main_character, menu)
    
    if atual_location in ["nitna_village"]:
        nitna_village.run()

    elif atual_location == "crossroads":
        pass

    menu_options = [
        "Menu",
        "Nitna Village",
        "Crossroads"
    ]

    key_actions = {
        "Menu": lambda: menu.run(), 
        "Crossroads": lambda: display_message(stdscr, "not_ready", 1000, curses.color_pair(1)),
        "Nitna Village": lambda: (update_game_state(atual_location="nitna_village"), nitna_village.run())
    }

    try:
        selected_index = 0
        while True:

            draw_menu(stdscr, "=== CHOOSE YOUR DESTINATION ===", menu_options, selected_index)

            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = max(0, selected_index - 1)  # Move a seleção para cima
            elif key == curses.KEY_DOWN:
                selected_index = min(len(menu_options) - 1, selected_index + 1)  # Move a seleção para baixo
            elif key == ord('\n'):  # Enter pressionado
                selected_option = menu_options[selected_index]
                action = key_actions.get(selected_option, lambda: display_message(stdscr, "Invalid choice. Try again.", 1000))
                action()  
                break
            
    except Exception as e:
        display_message(stdscr, f"Error while processing key press: {e}", 1000)

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
    nitna = game_state.get("nitna") if game_state.get("nitna") is not None else nitna

    update_game_state(main_character=main_character, prismeer=prismeer, cave=owl_bear_cave, nitna=nitna, atual_location = atual_location)
    
    while not should_exit():
        
        key_pressed_event(stdscr, main_character, prismeer, owl_bear_cave, nitna, atual_location, menu)

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
