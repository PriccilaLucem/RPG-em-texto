from destinations.prismeer.city import City
from characters.hero import Hero
from global_state.global_state import should_exit, set_exit  
from commands_allowed import  prismeer_commands
import curses

def city_menu(prismeer: City, main_character: Hero, ) -> None:
    input()
    while not should_exit():  
        print(
            f"""Choose your action:
            {prismeer_commands()}
            """
        )
        city_key = input("Where do you want to go? ").strip().upper()

        match city_key:
            case "Q":
                prismeer.billboard.billboard_menu(main_character)
            case "I":
                prismeer.inn.pass_the_night(main_character)
            case "C":
                visit_city_center(prismeer, main_character)
            case "E":
                print("Leaving Prismeer...\n")
                break
            case "EXIT":
                print("Exiting the game...\n")
                set_exit()  
            case "B":
                "Displaying inventory...\n"
                main_character.show_backpack()
            case _:
                print(f"Invalid choice. Try again. {city_key}\n")

def visit_city_center(prismeer: City, main_character: Hero, stdscr) -> None:
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    while not should_exit():
        stdscr.clear()
        stdscr.addstr("""
        Welcome to the city center:
        A - Visit the armor shop
        W - Visit the weapon shop
        E - Exit to city menu
        EXIT - Quit the game
        """)
        stdscr.refresh()

        center_key = stdscr.getch()  # Wait for user input

        # Handle the key press based on the user's input
        if center_key == ord('A'):
            prismeer.downtown.armor_shop.shop_interactions(main_character, stdscr)
        elif center_key == ord('W'):
            prismeer.downtown.weapon_shop.shop_interactions(main_character, stdscr)
        elif center_key == ord('E'):
            stdscr.clear()
            stdscr.addstr("Returning to city menu...\n")
            stdscr.refresh()
            curses.napms(1000)  # Wait for 1 second before returning
            break
        elif center_key == ord('X') or center_key == ord('Q'):  # EXIT or Quit the game
            stdscr.clear()
            stdscr.addstr("Exiting the game...\n")
            stdscr.refresh()
            set_exit()
            break
        else:
            stdscr.clear()
            stdscr.addstr("Invalid choice. Try again.\n")
            stdscr.refresh()
            curses.napms(1000)  # Wait for 1 second before clearing the error message