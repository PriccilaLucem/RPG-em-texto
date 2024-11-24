from destinations.prismeer.city import City
from characters.hero import Hero
from global_state.global_state import should_exit, set_exit  
from commands_allowed import  prismeer_commands
import curses

def city_menu(prismeer: City, main_character: Hero, stdscr: curses.window) -> None:
    curses.curs_set(0)  

    while not should_exit():
            stdscr.clear()
            stdscr.addstr("You are at Prismeer")
            stdscr.addstr(prismeer_commands())
            stdscr.refresh()
            city_key = stdscr.getch() 
            try:
                if city_key == ord('Q') or city_key == ord('q'):
                    prismeer.billboard.billboard_menu(stdscr, main_character)
                elif city_key == ord('I') or city_key == ord('i'):
                    prismeer.inn.pass_the_night(main_character)
                elif city_key == ord('C') or city_key == ord('c'):
                    visit_city_center(prismeer, main_character, stdscr)
                elif city_key == ord('E') or city_key == ord('e'):
                    stdscr.clear()
                    stdscr.addstr("Leaving Prismeer...\n")
                    stdscr.refresh()
                    curses.napms(1000) 
                    break

                elif city_key == ord('B') or city_key == ord('b'):
                    stdscr.clear()
                    stdscr.addstr("Displaying inventory...\n")
                    stdscr.addstr(main_character.show_backpack())  
                    stdscr.refresh()
                    stdscr.getch()  

                elif city_key == 27:
                    stdscr.clear()
                    stdscr.addstr("Exiting the game...\n")
                    stdscr.refresh()
                    set_exit()
                else:
                    stdscr.clear()
                    stdscr.addstr("Invalid choice. Try again.\n")
                    stdscr.refresh()
                    curses.napms(1000)
            except Exception as e:
                stdscr.clear()
                stdscr.addstr(f"An error occurred: {e}\n")
                stdscr.refresh()
                curses.napms(2000)



def visit_city_center(prismeer: City, main_character: Hero, stdscr: curses.window) -> None:
    curses.curs_set(0)  

    while not should_exit():
        stdscr.clear()
        stdscr.addstr(
            """Welcome to the city center:\n
            A - Visit the armor shop
            W - Visit the weapon shop
            E - Exit to city menu
            EXIT - Quit the game\n
            """
        )
        stdscr.refresh()

        try:
            center_key = stdscr.getch() 

            if center_key == ord('A') or center_key == ord('a'):
                prismeer.downtown.armor_shop.shop_interactions(main_character, stdscr)
            elif center_key == ord('W') or center_key == ord('w'):
                prismeer.downtown.weapon_shop.shop_interactions(main_character, stdscr)
            elif center_key == ord('E') or center_key == ord('e'):
                stdscr.clear()
                stdscr.addstr("Returning to city menu...\n")
                stdscr.refresh()
                curses.napms(1000)
                break
            elif center_key == 27:
                stdscr.clear()
                stdscr.addstr("Exiting the game...\n")
                stdscr.refresh()
                set_exit()
                break
            else:
                stdscr.clear()
                stdscr.addstr("Invalid choice. Try again.\n")
                stdscr.refresh()
                curses.napms(1000)
        except Exception as e:
            stdscr.clear()
            stdscr.addstr(f"An error occurred: {e}\n")
            stdscr.refresh()
            curses.napms(2000)
