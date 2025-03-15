import curses
from destinations.prismeer.city import City
from characters.hero import Hero
from destinations.prismeer import city_menu                                                                                   
from history.history import init_of_the_history
from global_state.global_state import set_exit, should_exit, update_game_state, get_game_state
from util.display_message import display_message
from destinations.cave import cave
from destinations.cave.owl_bear_cave import OwlBearCave
from destinations.forest.forest import Forest
from destinations.forest import forest
from menu.menu import menu    

def key_pressed_event(stdscr: curses.window, allow_enter_cave: bool, hero: Hero, prismeer: City, owl_bear_cave: OwlBearCave, wood_forest: Forest, atual_location:str):
    key_actions = {
        "P": lambda: (city_menu(prismeer, hero, stdscr, menu)),
        "F": lambda: (forest(wood_forest, hero, stdscr, menu)),
        "C": lambda: (cave(owl_bear_cave, hero, stdscr, menu)) if allow_enter_cave else display_message(stdscr, "Invalid choice. Try again.", 1000),
        "M": lambda: (menu(stdscr, hero, True)),    
    }
    if atual_location != "menu" and atual_location != "prismeer_surroundings":
        if atual_location == "prismeer" or atual_location == "city_center":
            city_menu(prismeer, hero, stdscr, menu)
        elif atual_location == "forest": 
            forest(wood_forest, hero, stdscr, menu)
        elif atual_location == "cave":
            cave(owl_bear_cave, hero, stdscr, menu)
    
    update_game_state(hero= hero, prismeer = prismeer, cave=owl_bear_cave, forest = wood_forest, atual_location= "prismeer_surroundings")
    
    try:
        render_ui(stdscr, allow_enter_cave)
        key = stdscr.getch()
        action = key_actions.get(chr(key).upper(), lambda: display_message(stdscr, "Invalid choice. Try again.", 1000))
        action()
    except Exception as e:
        display_message(stdscr, f"Error while processing key press: {e}", 1000)

def render_ui(stdscr: curses.window, allow_enter_cave: bool):
    stdscr.clear()
    stdscr.addstr(0, 0, "Game is running...\n")
    stdscr.addstr(1, 0, "Press any key (ESC to exit)...\n")
    stdscr.addstr(2, 0, "    M - Menu")
    stdscr.addstr(3, 0, "    S - View Status\n")
    stdscr.addstr(4, 0, "    P - Prismeer\n")
    stdscr.addstr(5, 0, "    F - Forest\n")
    if allow_enter_cave:
        stdscr.addstr(6, 0, "    C - OwlBear Cave\n")
    stdscr.refresh()

def game_loop(stdscr: curses.window, hero: Hero, prismeer: City, owl_bear_cave: OwlBearCave, wood_forest: Forest):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    menu(stdscr, hero, False)
    game_state = get_game_state()
    if game_state["is_new_game"]:
        history = init_of_the_history()
        display_message(stdscr, history, 5000)
        update_game_state(is_new_game=False)  
        atual_location = "prismeer_surroundings" 

    while not should_exit():
        hero, prismeer, owl_bear_cave, wood_forest, atual_location =  game_state["hero"], game_state["prismeer"], game_state["cave"], game_state["forest"], game_state["atual_location"]
        allow_enter_cave = any(
            quest.id == 1
            for quest in (hero.quests or []) + (hero.concluded_quests or [])
        )
        key_pressed_event(stdscr, allow_enter_cave, hero, prismeer, owl_bear_cave, wood_forest, atual_location)



def main(stdscr):
    hero = Hero()
    prismeer = City()
    owl_bear_cave = OwlBearCave()
    forest = Forest()
    update_game_state(hero=hero,prismeer=prismeer,cave= owl_bear_cave,forest=forest)
    
    
    try:
        game_loop(stdscr, hero, prismeer, owl_bear_cave, forest)
    except KeyboardInterrupt:
        print("Game interrupted.")
    finally:
        print("Goodbye!")

if __name__ == "__main__":
    curses.wrapper(main)
