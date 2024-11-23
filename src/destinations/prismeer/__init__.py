from destinations.prismeer.city import City
from characters.hero import Hero
from global_state.global_state import should_exit, set_exit  
from commands_allowed import  prismeer_commands, billboard_commands
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
                print(f"""
                You head to the billboard to see what's written.
                {billboard_commands()}
                """)
                billboard_key = input("What do you want to do?")
                match billboard_key:
                    case "Q":
                        curses.wrapper(prismeer.billboard.billboard_quests_menu, main_character)
                        print(main_character.show_active_quests())
                    case "N":
                        ...
                    case "EXIT":
                        set_exit()
                    case "B":
                        "Displaying inventory...\n"
                        main_character.show_backpack()
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

def visit_city_center(prismeer: City, main_character: Hero) -> None:
    while not should_exit():  
        print(
            """
            Welcome to the city center:
            A - Visit the armor shop
            W - Visit the weapon shop
            E - Exit to city menu
            EXIT - Quit the game
            """
        )
        center_key = input("Where do you want to go? ").strip().upper()

        match center_key:
            case "A":
                prismeer.downtown.armor_shop.shop_interactions(main_character)
            case "W":
                print(prismeer.downtown.weapon_shop.seller.speech(0))
            case "E":
                print("Returning to city menu...\n")
                break
            case "EXIT":
                print("Exiting the game...\n")
                set_exit()
            case _:
                print("Invalid choice. Try again.")
