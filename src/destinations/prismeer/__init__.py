from destinations.prismeer.city import City
from characters.hero import Hero
from global_state.global_state import should_exit, set_exit, update_game_state, exit_loop, get_game_state
from commands_allowed import prismeer_commands
from util.display_message import display_message
import curses

def city_menu(prismeer: City, main_character: Hero, stdscr: curses.window, menu) -> None:
    curses.curs_set(0)  
    atual_location = get_game_state()["atual_location"]
    if  atual_location == "city_center": 
        visit_city_center(prismeer, main_character, stdscr, menu)

    update_game_state(prismeer = prismeer, hero=main_character, atual_location = "prismeer")

    while not should_exit():
        try:
            stdscr.clear()
            stdscr.addstr("You are at Prismeer\n")
            stdscr.addstr(prismeer_commands())
            stdscr.refresh()
            city_key = stdscr.getch() 
            
            key_actions = {
                'B': lambda: prismeer.billboard.billboard_menu(stdscr, main_character),
                'I': lambda: prismeer.inn.pass_the_night(main_character, stdscr),
                'C': lambda: visit_city_center(prismeer, main_character, stdscr, menu),
                'Q': lambda: display_message(stdscr, "Leaving Prismeer...", 1000) or exit_loop("prismeer_surroundings"),
                'M': lambda: menu(stdscr, main_character, is_in_game=True),
            }
            
            action = key_actions.get(chr(city_key).upper(), lambda: display_message(stdscr, "Invalid choice. Try again.", 1000))
            action()
        except StopIteration:
            break
        except Exception as e:
            display_message(stdscr, f"An error occurred: {e}", 2000)

def visit_city_center(prismeer: City, main_character: Hero, stdscr: curses.window, menu) -> None:
    curses.curs_set(0)

    update_game_state(prismeer = prismeer, hero=main_character, atual_location = "city_center")

    while not should_exit():
        try:
            height, width = stdscr.getmaxyx()

            menu_options = [
                "Q - Exit to prismeer",
                "M - Show Menu",
                "A - Visit the armor shop",
                "W - Visit the weapon shop",
                "B - Talk to blacksmith",
                "1 - Talk to Afrac",
                "2 - Talk to Osvaldo",
                "3 - Talk to Damon",
                "4 - Talk to blacskmith",
                "EXIT - Quit the game",
            ]

            if height < len(menu_options) + 3:  
                menu_text = "\n".join(menu_options[-(height-3):]) 
            else:
                menu_text = "\n".join(menu_options)

            stdscr.clear()
            stdscr.addstr(0, 0, "Welcome to the city center:")
            stdscr.addstr(2, 0, menu_text)
            stdscr.refresh()

            center_key = stdscr.getch()

            key_actions = {
                'A': lambda: prismeer.downtown.armor_shop.shop_interactions(main_character, stdscr),
                'W': lambda: prismeer.downtown.weapon_shop.shop_interactions(main_character, stdscr),
                'Q': lambda: display_message(stdscr, "Returning to city menu...", 1000) or exit_loop("city_menu"),
                "B": lambda: prismeer.downtown.talk_to_blacksmith(stdscr, main_character),
                'M': lambda: menu(stdscr, main_character, True),
                27: lambda: (set_exit(), display_message(stdscr, "Exiting the game...")),
            }

            if chr(center_key).upper() in key_actions:
                key_actions[chr(center_key).upper()]()
            elif center_key == 27:
                key_actions[27]()
            elif center_key in {49, 50, 51, 52}:  # Keys 1, 2, 3, 4
                npc_response = prismeer.downtown.talk_to_npc(int(chr(center_key)), main_character)
                display_message(stdscr, npc_response, 2000)

                if center_key == 51 and prismeer.downtown.npcs[2].quest is not None:
                    display_message(stdscr, "Y - Accept the quest \nN - Deny the quest", 0)
                    quest_key = stdscr.getch()
                    if quest_key in {ord('Y'), ord('y')}:
                        prismeer.downtown.append_npc_quest(main_character, 3)
                        display_message(stdscr, "Quest Accepted", 1000)
            
                if center_key == 52:
                    if prismeer.downtown.npcs[3].quest is not None: 
                        blacksmith_response = prismeer.downtown.talk_to_npc(4, main_character)
                        if blacksmith_response == prismeer.downtown.npcs[3].speech(1):
                            display_message(stdscr, "Y - Accept the quest \nN - Deny the quest", 0)
                            user_input = stdscr.getch()
                            if user_input in {ord("Y"), ord("y")}:
                                prismeer.downtown.append_npc_quest(main_character, 4)  
                                display_message(stdscr, "Quest Accepted", 1000)
                            elif user_input in {ord("N"), ord("n")}:
                                display_message(stdscr, "Quest Denied", 1000)

                    elif prismeer.downtown.npcs[3].quest is None:  
                        if any(quest.id == 2 for quest in main_character.quests):
                            display_message(stdscr, "Blacksmith: How's the progress on the quest?", 1000)
                            display_message(stdscr, "Deliver the quest items? Y/N", 500)
                            user_input = stdscr.getch()
                            if user_input in {ord("Y"), ord("y")}:
                                try:
                                    quest = main_character.find_quest_by_id(2)
                                    main_character.remove_items_from_backpack(quest.items_to_be_collected)
                                    display_message(stdscr, f"{prismeer.downtown.npcs[3].name}: Thank you, Hero! Here's your reward.", 1000)
                                    main_character.conclude_quests(quest)
                                    prismeer.downtown.talk_to_npc(4,main_character)
                                except ValueError as e:
                                    display_message(stdscr, str(e), 1000)
                            elif user_input in {ord("N"), ord("n")}:
                                display_message(stdscr, f"{prismeer.downtown.npcs[3].name}: Come back when you have the items.", 1000)
                        else:
                            display_message(stdscr, prismeer.downtown.talk_to_npc(4))
        except StopIteration:
            break
        except Exception as e:
            display_message(stdscr, f"An error occurred: {e}", 2000)
