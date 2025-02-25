from destinations.cave.owl_bear_cave import OwlBearCave
from characters.hero import Hero
from global_state.global_state import should_exit, set_exit
from commands_allowed import cave_commands, inside_cave_commands, mine_cave_commands
import curses
from util.display_message import display_message
from util.combat_system import combat
from history.history import the_real_init
from resources import mine

def exit_loop():
    raise StopIteration

def cave(owl_bear_cave: OwlBearCave, main_character: Hero, stdscr: curses.window) -> None:
    curses.curs_set(0)

    actions = {
        chr(10): lambda: display_message(stdscr, "Entering cave...", 1000) or inside_the_cave(stdscr, main_character, owl_bear_cave),
        "S": lambda: main_character.show_status(stdscr),
        "E": lambda: display_message(stdscr, "Returning to previous menu...", 1000) or exit_loop(),
        chr(27): lambda: display_message(stdscr, "Exiting the game...", 1000) or set_exit()
    }


            

    while not should_exit():
        try:
            stdscr.clear()
            stdscr.addstr(cave_commands())
            stdscr.refresh()

            owl_bear_cave_key = stdscr.getch()

            action = actions.get(chr(owl_bear_cave_key).upper(), lambda: display_message(stdscr, "Invalid choice. Try again.", 1000)) 
            action()
        except StopIteration:
            break
        except Exception as e:   
            display_message(stdscr, f"An error occurred: {e}", 2000)


def inside_the_cave(stdscr: curses.window, main_character: Hero, owl_bear_cave: OwlBearCave) -> None:
    combat_done = False

    def npc_interactions():
        while not should_exit():
            try:
                stdscr.clear()
                stdscr.addstr(inside_cave_commands())  
                stdscr.refresh()
                
                owl_bear_cave_key = stdscr.getch()
                action = actions.get(
                    chr(owl_bear_cave_key).upper(),
                    lambda: display_message(stdscr, "Invalid choice. Try again.", 1000)
                )
                action()
            except StopIteration:
                break
            except Exception as e:
                display_message(stdscr, f"An error occurred: {e}", 2000)

    actions = {
        "S": lambda: main_character.show_status(stdscr),
        "E": lambda: display_message(stdscr, "Returning to outside the cave...", 1000) or exit_loop(),
        "1": lambda: display_message(stdscr, owl_bear_cave.talk_to_npc(1), 1000),
        "2": lambda: display_message(stdscr, owl_bear_cave.talk_to_npc(2), 1000),
        "3": lambda: display_message(stdscr, owl_bear_cave.owl_bear.drop_items(main_character), 3000),
        chr(27): lambda: display_message(stdscr, "Exiting the game...", 1000) or set_exit(),
    }

    while not should_exit():
        if not combat_done and any(quest.id == 1 for quest in main_character.quests):
            combat_done = True  
            intro_message = """
            As you enter the cave, you see two people staring at you, nervously.
            They are looking behind you!
            The OwlBear is angry at you and starts running into your direction!
            """
            display_message(stdscr, intro_message, 3000)

            if not combat(stdscr, main_character, owl_bear_cave.owl_bear):
                display_message(stdscr, the_real_init(), 3000)
                main_character.choose_character_class(stdscr)

                display_message(stdscr, (
                    "You wake up to Damon’s brothers frantically trying to wake you up. "
                    "As you look to the side, you see the lifeless body of the OwlBear and wonder how it all happened..."
                ), 5000)
    
                main_character.health_points = main_character.max_hp
                quest_to_remove = next((quest for quest in main_character.quests if quest.id == 1), None)
                if quest_to_remove:
                    main_character.conclude_quests(quest_to_remove)
                    main_character.quests.remove(quest_to_remove)

                npc_interactions() 
        else:
            while not should_exit():
                stdscr.clear()
                stdscr.addstr(mine_cave_commands())
                stdscr.refresh()
                actions = {
                    "S": lambda: main_character.show_status(stdscr),
                    "E": lambda: display_message(stdscr, "Returning to outside the cave...", 1000) or exit_loop(),
                    "M": lambda: (
                        display_message(stdscr, "You have already mined this turn.", 1000)
                        if owl_bear_cave.has_already_mined
                        else setattr(owl_bear_cave, "has_already_mined", mine(stdscr, owl_bear_cave.ores, main_character))
                    ),
                    chr(27): lambda: display_message(stdscr, "Exiting the game...", 1000) or set_exit(),
                }
                owl_bear_cave_key = stdscr.getch()
                action = actions.get(
                    chr(owl_bear_cave_key).upper(),
                    lambda: display_message(stdscr, "Invalid choice. Try again.", 1000)
                )
                action()

                