from typing import List
import curses
from quests.quests import Quests
from quests import generate_random_quests
from characters.hero import Hero
from commands_allowed import billboard_commands
from global_state.global_state import set_exit,should_exit

class Billboard():
    def __init__(self) -> None:
        self.quests: List[Quests] = generate_random_quests()

    def billboard_menu(self, stdscr: curses.window, main_character: Hero) -> None:
        curses.curs_set(0)
        stdscr.clear()
        
        stdscr.addstr("You head to the billboard to see what's written.\n")
        stdscr.addstr(billboard_commands())
        stdscr.refresh()
    
        while not should_exit():  
            stdscr.clear()
            stdscr.addstr("You head to the billboard to see what's written.\n")
            stdscr.addstr(billboard_commands())
            stdscr.refresh()
        
            key = stdscr.getch() 
    
            if key == ord('Q') or key == ord('q'):  
                self.show_quests(stdscr, main_character)
            elif key == ord('I') or key == ord('i'):  
                stdscr.clear()  
                stdscr.addstr(main_character.show_backpack())
                stdscr.refresh()
                curses.napms(1000)  
            elif key == ord("N") or key == ord("n"):  
                pass
            elif key == ord("E") or key == ord("e"):  
                stdscr.clear()
                stdscr.addstr("You pressed E. Exiting quest selection.\n")
                stdscr.refresh()
                curses.napms(1000)
                break
            elif key == 27:  
                set_exit()
            else:
                stdscr.clear()                
                stdscr.refresh()
                stdscr.addstr("You pressed an invalid key.\n")
    
    
    
    def show_quests(self, stdscr: curses.window, main_character: Hero) -> None:
        """Display all available quests on the billboard."""
        if not self.quests:
            stdscr.clear()
            stdscr.addstr("No quests available.\n")
            stdscr.refresh()
            stdscr.getch()
            return

        curses.curs_set(0) 
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        selected_index = 0

        while not should_exit():
            stdscr.clear()
            stdscr.addstr("Available Quests:\n")

            for idx, quest in enumerate(self.quests):
                if idx == selected_index:
                    stdscr.addstr(f"--> {quest.__str__()}\n", curses.color_pair(1))
                else:
                    stdscr.addstr(f"    {quest.__str__()}\n")

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and selected_index > 0:
                selected_index -= 1
            elif key == curses.KEY_DOWN and selected_index < len(self.quests) - 1:
                selected_index += 1
            elif key == 10: 
                selected_quest = self.quests[selected_index]
                stdscr.clear()
                stdscr.addstr(f"You selected: {selected_quest}\n")
                stdscr.refresh()

                main_character.append_quests(self.get_quest_from_billboard(selected_index))
                self.quests.pop(selected_index)  
                stdscr.addstr(f"Quest '{selected_quest}' added to your journal!\n")
                stdscr.refresh()
                curses.napms(1000)  
                break
            elif key == 27:
                stdscr.clear()
                stdscr.addstr("You pressed ESC. Exiting quest selection.\n")
                stdscr.refresh()
                curses.napms(1000)
                break  
            elif key == ord('Q'):
                self.billboard_menu(stdscr, main_character) 

    def get_quest_from_billboard(self, index: int) -> Quests:
        """Return the quest at the specified index without removing it."""
        return self.quests[index]
