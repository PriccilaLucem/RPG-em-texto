from characters.hero import Hero
import curses
class Inn:
    def __init__(self, cost: int, name) -> None:
        self.cost = cost
        self.name = name
    
    def pass_the_night(self, main_character: Hero, stdscr:curses.window ) -> None:
        stdscr.clear()
        stdscr.refresh()
        while True:
            stdscr.addstr(f"You entered the {self.name}. Would you like to rest?\n")
            stdscr.addstr("Y - Yes\nN - No\n")
            inn_choice = stdscr.getch()
            if inn_choice == ord("Y") or inn_choice == ord("y"):

                if main_character.gold < self.cost:
                    stdscr.addstr("You don't have enough gold!")
                    stdscr.refresh()
                else:
                    main_character.gold -= self.cost
                    main_character.hp = main_character.max_hp
                    stdscr.addstr(f"You rested at the inn. Remaining gold: {main_character.gold}")
                    stdscr.refresh()
                curses.napms(2000)
                break
            elif inn_choice == ord("N") or inn_choice == ord("n"):
                stdscr.addstr("You chose not to rest.\n")
                stdscr.refresh()
                curses.napms(2000)
                break
            else:
                    stdscr.clear()
                    stdscr.addstr("Invalid choice. Try again.\n")
                    stdscr.refresh()
                    curses.napms(1000)
                    stdscr.clear()
                
                