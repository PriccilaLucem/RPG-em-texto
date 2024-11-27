from destinations.prismeer.city import City
from characters.hero import Hero
from global_state.global_state import should_exit, set_exit  
from commands_allowed import prismeer_commands
from util.display_message import display_message
import curses


def city_menu(prismeer: City, main_character: Hero, stdscr: curses.window) -> None:
    curses.curs_set(0)  

    while not should_exit():
        try:
            stdscr.clear()
            stdscr.addstr("You are at Prismeer\n")
            stdscr.addstr(prismeer_commands())
            stdscr.refresh()
            city_key = stdscr.getch() 
            
            key_actions = {
                'Q': lambda: prismeer.billboard.billboard_menu(stdscr, main_character),
                'I': lambda: prismeer.inn.pass_the_night(main_character, stdscr),
                'C': lambda: visit_city_center(prismeer, main_character, stdscr),
                'B': lambda: display_message(stdscr, "Displaying inventory...\n" + main_character.show_backpack()),
                'E': lambda: display_message(stdscr, "Leaving Prismeer...", 1000),
                27: lambda: (set_exit(), display_message(stdscr, "Exiting the game...")),
            }
            
            if city_key in {ord('e'), ord('E')}:
                key_actions['E']()
                break
            elif chr(city_key).upper() in key_actions:
                key_actions[chr(city_key).upper()]()
            elif city_key == 27:
                key_actions[27]()            
            else:
                display_message(stdscr, "Invalid choice. Try again.")
        except Exception as e:
            display_message(stdscr, f"An error occurred: {e}", 2000)

def visit_city_center(prismeer: City, main_character: Hero, stdscr: curses.window) -> None:
    curses.curs_set(0)

    while not should_exit():
        try:
            display_message(stdscr, 
                """Welcome to the city center:\n
                A - Visit the armor shop
                W - Visit the weapon shop
                E - Exit to city menu
                1 - Talk to Afrac
                2 - Talk to Osvaldo
                3 - Talk to Damon
                EXIT - Quit the game\n""", 
                0)

            center_key = stdscr.getch()
            
            key_actions = {
                'A': lambda: prismeer.downtown.armor_shop.shop_interactions(main_character, stdscr),
                'W': lambda: prismeer.downtown.weapon_shop.shop_interactions(main_character, stdscr),
                'E': lambda: display_message(stdscr, "Returning to city menu...", 1000) or exit_loop(),
                27: lambda: (set_exit(), display_message(stdscr, "Exiting the game...")),
            }
            
            def exit_loop():
                raise StopIteration
            
            if chr(center_key).upper() in key_actions:
                key_actions[chr(center_key).upper()]()
            elif center_key == 27:
                key_actions[27]()
            elif center_key in {49, 50, 51}:  # Teclas 1, 2, 3
                npc_response = prismeer.downtown.talk_to_npc(int(chr(center_key)), main_character)
                display_message(stdscr, npc_response, 2000)

                if center_key == 51 and prismeer.downtown.npcs[2].quest != None:
                    display_message(stdscr, "Y - Accept the quest \nN - Deny the quest", 0)
                    quest_key = stdscr.getch()
                    if quest_key in {ord('Y'), ord('y')}:
                        prismeer.downtown.append_npc_quest(main_character)
                        display_message(stdscr, "Quest Accepted")
            else:
                display_message(stdscr, "Invalid choice. Try again.")
        except StopIteration:
            break
        except Exception as e:
            display_message(stdscr, f"An error occurred: {e}", 2000)
