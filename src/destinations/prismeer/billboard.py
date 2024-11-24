from typing import List
import curses
from quests.quests import Quests
from quests import generate_random_quests
from characters.hero import Hero
from commands_allowed import billboard_commands
from global_state.global_state import set_exit
from characters.hero import Hero

class Billboard():
    def __init__(self) -> None:
        self.quests: List[Quests] = generate_random_quests()
    
    def billboard_menu(self, main_character:Hero) -> None:
        print(f"""
                You head to the billboard to see what's written.
                {billboard_commands()}
                """)
        billboard_key = input("What do you want to do?")
        match billboard_key:
            case "Q":
                curses.wrapper(self.billboard_quests_menu, main_character)
            case "N":
                ...
            case "EXIT":
                set_exit()
            case "B":
                "Displaying inventory...\n"
                main_character.show_backpack()
    
    def show_quests(self) -> None:
        """Print all available quests."""
        for quest in self.quests:
            print(quest.__str__())

    def get_quest_from_billboard(self, index: int) -> Quests:
        """Return the quest at the specified index without removing it."""
        return self.quests[index]

    def billboard_quests_menu(self, stdscr, main_character:Hero) -> None:
        """Display and interact with the quests menu."""
        def draw_quests(stdscr, quests, selected_index):
            """Draw the quests menu with the selected index highlighted."""
            stdscr.clear()
            stdscr.addstr("Available Quests:\n")
            for idx, quest in enumerate(quests):
                if idx == selected_index:
                    stdscr.addstr(f"--> {quest}\n", curses.color_pair(1)) 
                else:
                    stdscr.addstr(f"    {quest}\n")
            stdscr.refresh()

        curses.curs_set(0)  
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 

        if not self.quests:
            stdscr.addstr("No quests available.\n")
            stdscr.refresh()
            return

        selected_index = 0 

        while True:
            draw_quests(stdscr, self.quests, selected_index)

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
            elif key == 27:  
                break
