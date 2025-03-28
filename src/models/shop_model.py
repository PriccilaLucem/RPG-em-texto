import curses
from typing import List, Dict, Any
from characters.main_character import MainCharacter
from global_state.global_state import should_exit
from util.display_message import display_message, draw_menu
from util.classes import ITEM_CLASSES
from models.npc_model import Seller_model


class Shop_model:
    def __init__(self, name: str, seller_name: str, speeches: List[str], backpack, stdscr: curses.window) -> None:
        self.name = name
        self.seller = Seller_model(seller_name, speeches, backpack)
        self.stdscr = stdscr
    
    def shop_interactions(self, main_character: "MainCharacter") -> None:
        selected_index = 0
        options = [
            "Show Shop Inventory",
            "Talk to Seller",
            "Exit Shop",
        ]

        while True:
            draw_menu(self.stdscr, f"Welcome to {self.name}!", options, selected_index)
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif options[selected_index] == "Exit Shop":
                display_message(self.stdscr, "Thank you for visiting! Come again.", 1000, curses.color_pair(11))
                break
            elif key == 10:  
                self.handle_menu_option(options[selected_index], main_character)
            

    def handle_menu_option(self, option: str, main_character:  "MainCharacter") -> None:
        """Handles the selected menu option."""
        if option == "Show Shop Inventory":
            self.show_inventory(main_character)
        elif option == "Talk to Seller":
            self.talk_to_seller()
            
    def show_inventory(self, main_character:  "MainCharacter") -> None:
        """Exibe o inventário da loja com navegação e opção de compra."""
        if not self.seller.backpack:
            display_message(self.stdscr, "The shop is out of stock!", 1000, curses.color_pair(2))  # Usa color_pair(2) para o texto
            return

        selected_index = 0
        items = self.seller.backpack
        title = f"=== ITEMS FOR SALE IN {self.name} ==="

        while True:
            # Prepara a lista de itens para exibição
            items_to_show = [
                item.__str__() for item in items
            ]
            items_to_show.append("Exit")
            # Desenha o menu com os itens disponíveis
            draw_menu(self.stdscr, title, items_to_show, selected_index)

            # Captura a tecla pressionada
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(items_to_show)  # Navega para cima
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(items_to_show)  # Navega para baixo
            elif key == 10:  # Tecla ENTER
                if items_to_show[selected_index] == "Exit":
                    break
                self.buy_item(selected_index, main_character)  
                if not self.seller.backpack:  # Se o inventário estiver vazio após a compra
                    display_message(self.stdscr, "The shop is out of stock!", 1000, curses.color_pair(2))
                    break
                
            
    
    
    def buy_item(self, selected_index: int, main_character: "MainCharacter") -> None:
        """Handles the purchase of an item."""
        selected_item = self.seller.backpack[selected_index]
        if main_character.gold >= selected_item.value:
            main_character.gold -= selected_item.value
            main_character.backpack.append(selected_item)
            self.seller.backpack.remove(selected_item)
            display_message(self.stdscr, f"You bought {selected_item.name} for {selected_item.value} gold!", 1000)
        else:
            display_message(self.stdscr, "You don't have enough gold to buy this item.", 1000)
    
    def talk_to_seller(self) -> None:
        """
        Interage com o vendedor, permitindo ao jogador ouvir suas falas.
        """
        if not self.seller.speeches:
            display_message(self.stdscr, "The seller has nothing to say.", 1000, curses.color_pair(2))  # Usa color_pair(2) para o texto
            return
    
        seller_title = f"=== {self.seller.name} ==="
        self.speech_index = 0  # Inicializa o índice da fala
    
        while True:
            speech = self.seller.speech(self.speech_index)
    
            draw_menu(self.stdscr, seller_title, [speech], 0, "Press ENTER to continue, 'Q' to quit")
    
            key = self.stdscr.getch()
    
            if key == 10:  # Tecla ENTER
                if self.speech_index < len(self.seller.speeches) - 1:
                    self.speech_index += 1  
                else:
                    break  
            elif key == ord('q') or key == ord('Q'):
                break
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Shop_model':
        backpack = []

        for item_data in data.get("backpack", []):
            if not isinstance(item_data, dict):
                raise ValueError(f"Invalid item data: {item_data}. Expected a dictionary.")
            item_type = item_data.get("type")
            if not item_type:
                raise ValueError(f"Missing item type in {item_data}")
            if item_type in ITEM_CLASSES:
                item_class = ITEM_CLASSES[item_type]
                del item_data["type"]
                backpack.append(item_class.from_dict(item_data))
            else:
                raise ValueError(f"Unknown item type: {item_type}")
        return cls(
            name = data["name"],
            speeches = data["speeches"],
            backpack = backpack,
            seller_name = data["seller_name"]
        )
        
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts the Shop_model instance to a dictionary."""
        return {
            'name': self.name,
            'seller_name': self.seller.name if self.seller else None,
            'speeches': self.seller.speeches if self.seller else [],
            'backpack': [
            {
                'type': item.__class__.__name__, 
                **item.to_dict()  
            }
            for item in getattr(self.seller, 'backpack', []) if hasattr(item, 'to_dict')
        ]
      }   