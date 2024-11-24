import curses
from models.seller_model import Seller_model
from characters.hero import Hero

class Shop_model():
    def __init__(self, name: str, seller_name: str, speeches: list, backpack: list) -> None:
        self.seller = Seller_model(seller_name, speeches, backpack)
        self.name = name

    def shop_interactions(self, main_character: Hero, stdscr) -> None:
        curses.curs_set(0)  # Hide the cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlighted text color
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Normal text color

        shop_speech = 0
        while True:
            stdscr.clear()
            stdscr.addstr(f"You entered the {self.name} shop. What would you like to do?\n")
            stdscr.addstr("T - Talk to the seller\n")
            stdscr.addstr("B - Buy items\n")
            stdscr.addstr("E - Leave the shop\n")
            stdscr.refresh()

            shop_key = stdscr.getch()

            if shop_key == ord('T'):
                # Talk to the seller
                if shop_speech < len(self.seller.speeches):
                    stdscr.clear()
                    stdscr.addstr(self.seller.speech(shop_speech))
                    shop_speech += 1
                else:
                    stdscr.clear()
                    stdscr.addstr(self.seller.speech(-1))  # End of seller's speeches
                stdscr.refresh()
                stdscr.getch()  # Wait for user to press a key before returning to the menu

            elif shop_key == ord('B'):
                # Buy items
                stdscr.clear()
                if not self.seller.inventory:
                    stdscr.addstr("The shop is out of stock!\n")
                else:
                    stdscr.addstr("Available items for sale:\n")
                    for idx, item in enumerate(self.seller.inventory):
                        stdscr.addstr(f"{idx + 1}. {item.name} - {item.price} gold\n")
                    stdscr.addstr("\nUse UP/DOWN arrows to navigate and ENTER to select an item.\n")
                    stdscr.refresh()

                    selected_index = 0  # Start at the top of the list
                    while True:
                        stdscr.clear()
                        stdscr.addstr("Available items for sale:\n")
                        for idx, item in enumerate(self.seller.inventory):
                            if idx == selected_index:
                                stdscr.addstr(f"--> {item.name} - {item.price} gold\n", curses.color_pair(1))  # Highlight selected item
                            else:
                                stdscr.addstr(f"    {item.name} - {item.price} gold\n", curses.color_pair(2))  # Normal items
                        stdscr.refresh()

                        key = stdscr.getch()  # Get user input

                        if key == curses.KEY_UP and selected_index > 0:
                            selected_index -= 1
                        elif key == curses.KEY_DOWN and selected_index < len(self.seller.inventory) - 1:
                            selected_index += 1
                        elif key == 10:  # Enter key to select an item
                            selected_item = self.seller.inventory[selected_index]
                            if main_character.gold >= selected_item.price:
                                main_character.gold -= selected_item.price
                                main_character.add_item(selected_item)
                                stdscr.clear()
                                stdscr.addstr(f"You bought {selected_item.name} for {selected_item.price} gold!\n")
                                stdscr.refresh()
                                curses.napms(1000)  # Wait for a second before returning to the shop menu
                                break  # Exit buying items menu
                            else:
                                stdscr.clear()
                                stdscr.addstr("You don't have enough gold.\n")
                                stdscr.refresh()
                                curses.napms(1000)  # Wait for a second before returning to the shop menu
                                break  # Exit buying items menu
                        elif key == 27:  # Escape key to exit the buying items menu
                            break  # Exit buying items menu

            elif shop_key == ord('E'):
                # Exit shop
                stdscr.clear()
                stdscr.addstr("You are leaving the shop...\n")
                stdscr.refresh()
                curses.napms(1000)
                break  # Exit the shop

            else:
                # Invalid key pressed
                continue
