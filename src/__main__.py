import curses
from destinations.prismeer.city import City
from characters.hero import Hero
from destinations.prismeer import CityMenu
from history.history import init_of_the_history
from global_state.global_state import should_exit, update_game_state, get_game_state
from util.display_message import display_message, draw_menu, draw_menu_with_history
from destinations.cave.owl_bear_cave import OwlBearCave
from destinations.cave import OutsideCave
from destinations.forest.forest import Forest
from destinations.forest import ForestMenu
from menu.menu import Menu


def key_pressed_event(stdscr: curses.window, allow_enter_cave: bool, hero: Hero, prismeer: City, owl_bear_cave: OwlBearCave, wood_forest: Forest, atual_location: str, menu: Menu):
    """Handles key press events and triggers corresponding actions."""
    update_game_state(is_in_game=True)  # Atualiza o estado global


    # Inicializa os menus
    city_menu = CityMenu(prismeer, hero, stdscr, menu)
    forest_menu = ForestMenu(wood_forest, hero, stdscr, menu)
    owl_bear_cave_menu = OutsideCave(owl_bear_cave, hero, stdscr, menu)

    # Executa o menu correspondente à localização atual
    if atual_location not in ["menu", "prismeer_surroundings"]:
        if  atual_location in ["prismeer", "prismeer_center"]:
            city_menu.run()
        elif atual_location == "forest":
            forest_menu.run()
        elif atual_location in ["inside_owl_bear_cave", "outside_owl_bear_cave"]:
            owl_bear_cave_menu.run()

    # Define as ações com base nas opções do menu
    key_actions = {
        "Menu": (lambda: menu.run()),  # Abre o menu principal
        "Prismeer": lambda: (update_game_state(atual_location="prismeer") or city_menu.run()), 
        "Forest": lambda: (update_game_state(atual_location="forest") or forest_menu.run()),  
        "Owl Bear Cave": lambda: (update_game_state(atual_location="outside_owl_bear_cave"), owl_bear_cave_menu.run())  # Vai para a Caverna do Owl Bear
    }

    # Atualiza o estado do jogo
    update_game_state(hero=hero, prismeer=prismeer, cave=owl_bear_cave, forest=wood_forest, atual_location="prismeer_surroundings", is_in_game = True)

    try:
        selected_index = 0
        while True:
            # Renderiza a interface do usuário
            render_ui(stdscr, allow_enter_cave, selected_index)

            # Obtém a entrada do usuário
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = max(0, selected_index - 1)  # Move a seleção para cima
            elif key == curses.KEY_DOWN:
                menu_options = get_menu_options(allow_enter_cave)
                selected_index = min(len(menu_options) - 1, selected_index + 1)  # Move a seleção para baixo
            elif key == ord('\n'):  # Tecla ENTER
                menu_options = get_menu_options(allow_enter_cave)
                selected_option = menu_options[selected_index]
                action = key_actions.get(selected_option, lambda: display_message(stdscr, "Invalid choice. Try again.", 1000))
                action()  # Executa a ação correspondente
                break
    except Exception as e:
        display_message(stdscr, f"Error while processing key press: {e}", 1000)

def get_menu_options(allow_enter_cave: bool) -> list:
    """Returns a list of menu options with their corresponding action keys."""
    menu_options = [
        "Menu",
        "Prismeer",
        "Forest"
    ]
    if allow_enter_cave:
        menu_options.append("Owl Bear Cave")
    return menu_options


def render_ui(stdscr: curses.window, allow_enter_cave: bool, selected_index: int):
    """Renders the game UI with the selected menu option highlighted."""
    stdscr.clear()
    menu_options = get_menu_options(allow_enter_cave)
    draw_menu(stdscr, "Game is running...", menu_options, selected_index)
    stdscr.refresh()

def game_loop(stdscr: curses.window, hero: Hero, prismeer: City, owl_bear_cave: OwlBearCave, wood_forest: Forest):
    """Main game loop."""
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    menu = Menu(stdscr, prismeer, False)
    menu.run()

    game_state = get_game_state()
    
    if game_state["is_new_game"]:
        history = init_of_the_history()
        title = "=== IN SOMEWHERE NEAR PRISMMER ==="
        options = ["Continue"]
        selected_index = 0

        while True:
            draw_menu_with_history(stdscr,title,history, options, selected_index )
            key = stdscr.getch()
            if key == 10:  # ENTER
                break
        update_game_state(is_new_game=False)
        atual_location = "prismeer_surroundings"
    else:
        hero, prismeer, owl_bear_cave, wood_forest, atual_location = (
            game_state["hero"],
            game_state["prismeer"],
            game_state["cave"],
            game_state["forest"],
            game_state["atual_location"]
        )

    while not should_exit():
        allow_enter_cave = any(
            quest.id == 1
            for quest in (hero.quests or []) + (hero.concluded_quests or [])
        )
        key_pressed_event(stdscr, allow_enter_cave, hero, prismeer, owl_bear_cave, wood_forest, atual_location, menu)


def main(stdscr):
    """Initializes the game and starts the main loop."""
    hero = Hero()
    prismeer = City()
    owl_bear_cave = OwlBearCave()
    forest = Forest()
    update_game_state(hero=hero, prismeer=prismeer, cave=owl_bear_cave, forest=forest)

    try:
        game_loop(stdscr, hero, prismeer, owl_bear_cave, forest)
    except KeyboardInterrupt:
        print("Game interrupted.")
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    curses.wrapper(main)