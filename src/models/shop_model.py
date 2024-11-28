import curses
from typing import List
from models.seller_model import Seller_model
from characters.hero import Hero
from global_state.global_state import should_exit, set_exit
from commands_allowed import shop_commands

class Shop_model:
    def __init__(self, name: str, seller_name: str, speeches: List[str], backpack) -> None:
        self.name = name
        self.seller = Seller_model(seller_name, speeches, backpack)

    def shop_interactions(self, main_character: Hero, stdscr: curses.window) -> None:
        """Exibe o menu principal do Shop."""
        curses.curs_set(0)
        stdscr.clear()

        stdscr.addstr(f"Welcome to {self.name}!\n")
        stdscr.addstr(shop_commands())
        stdscr.refresh()
        speech_accounted = 0
        while not should_exit():
            stdscr.clear()  
            stdscr.addstr(f"Welcome to {self.name}!\n")
            stdscr.addstr(shop_commands())
            stdscr.refresh()

            key = stdscr.getch()

            if key in {ord('s'), ord('S')}:  
                self.show_inventory(stdscr, main_character)
            elif key in {ord("B"), ord("b")}:
                    stdscr.clear()
                    stdscr.addstr("Displaying inventory...\n")
                    stdscr.addstr(main_character.show_inventory())  
                    stdscr.refresh()
                    stdscr.getch()
            elif key in {ord('E'), ord('e')}:  
                stdscr.clear()
                stdscr.addstr("Thank you for visiting! Come again.\n")
                stdscr.refresh()
                curses.napms(1000)
                break
            elif key in {ord("T"), ord("t")}:
                if speech_accounted < len(self.seller.speeches):
                    stdscr.clear()
                    stdscr.addstr(self.seller.speech(speech_accounted))
                    speech_accounted += 1
                    stdscr.refresh()
                    curses.napms(2000)
                else:
                    stdscr.clear()
                    stdscr.addstr(self.seller.speech(2))
                    stdscr.refresh()
                    curses.napms(2000)
            elif key == 27: 
                set_exit()
            else:
                stdscr.clear()
                stdscr.addstr("Invalid key pressed. Try again.\n")
                stdscr.refresh()
                curses.napms(1000)


    def show_inventory(self, stdscr: curses.window, main_character: Hero) -> None:
        """Displays the available items in the shop with scrolling."""
        if not self.seller.backpack:
            stdscr.clear()
            stdscr.addstr("The shop is out of stock!\n")
            stdscr.refresh()
            stdscr.getch()
            return

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        selected_index = 0 
        max_height, max_width = stdscr.getmaxyx() 
        item_list_height = max_height - 4 

        items = self.seller.backpack

        while not should_exit():
            stdscr.clear()

            stdscr.addstr(f"Items for Sale in {self.name}\n")
            stdscr.addstr(f"Use UP/DOWN arrows to navigate, ENTER to buy, ESC to exit\n")

            start_idx = selected_index - (selected_index % item_list_height)
            end_idx = min(start_idx + item_list_height, len(self.seller.backpack))
            for idx in range(start_idx, end_idx):
                item = items[idx]
                if idx == selected_index:
                    stdscr.addstr(f"--> {item.__str__()}\n", curses.color_pair(1))
                else:
                    stdscr.addstr(f"    {item.__str__()}\n")

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and selected_index > 0:
                selected_index -= 1  
            elif key == curses.KEY_DOWN and selected_index < len(items) - 1:
                selected_index += 1  
            elif key == 10:  
                selected_item = items[selected_index]
                stdscr.clear()

                if main_character.gold >= selected_item.value:
                    main_character.gold -= selected_item.value
                    main_character.backpack.append(selected_item)
                    self.seller.backpack.remove(selected_item)
                    stdscr.addstr(f"You bought {selected_item.name} for {selected_item.value} gold!\n")
                else:
                    stdscr.addstr("You don't have enough gold to buy this item.\n")

                stdscr.refresh()
                curses.napms(1000)
            elif key == 27:  
                stdscr.clear()
                stdscr.addstr("Exiting shop inventory.\n")
                stdscr.refresh()
                curses.napms(1000)
                break
            elif key in {ord('M'), ord('m')}: 
                self.shop_interactions(stdscr, main_character)
                break
