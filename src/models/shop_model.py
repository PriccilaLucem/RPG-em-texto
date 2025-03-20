import curses
from typing import List, Dict, Any
from models.seller_model import Seller_model
from characters.hero import Hero
from global_state.global_state import should_exit
from util.display_message import display_message, draw_menu
from util.classes import ITEM_CLASSES
from models.seller_model import Seller_model


class Shop_model:
    def __init__(self, name: str, seller_name: str, speeches: List[str], backpack) -> None:
        self.name = name
        self.seller = Seller_model(seller_name, speeches, backpack)

    def shop_interactions(self, main_character: Hero, stdscr: curses.window) -> None:
        """Main loop for shop interactions."""
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Normal text
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlighted text
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Titles and borders

        selected_index = 0
        options = [
            "Show Shop Inventory",
            "Talk to Seller",
            "Exit Shop",
        ]

        while not should_exit():
            draw_menu(stdscr, f"Welcome to {self.name}!", options, selected_index)
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif options[selected_index] == "Exit Shop":
                display_message(stdscr, "Thank you for visiting! Come again.", 1000)
                break
            elif key == 10:  # Enter key
                self.handle_menu_option(options[selected_index], main_character, stdscr)
            

    def handle_menu_option(self, option: str, main_character: Hero, stdscr: curses.window) -> None:
        """Handles the selected menu option."""
        if option == "Show Shop Inventory":
            self.show_inventory(stdscr, main_character)
        elif option == "Talk to Seller":
            self.talk_to_seller(stdscr)
            
    def show_inventory(self, stdscr: curses.window, main_character: Hero) -> None:
        """Exibe o inventário da loja com navegação e opção de compra."""
        if not self.seller.backpack:
            display_message(stdscr, "The shop is out of stock!", 1000)
            return
    
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Item selecionado
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Itens normais
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Títulos e bordas
    
        selected_index = 0
        offset = 0  # Índice de deslocamento para navegação
        items_to_show = self.seller.show_backpack()
        items = self.seller.backpack
     
        while not should_exit():
            stdscr.clear()
            height, width = stdscr.getmaxyx()
    
            # Título
            title = f"Items for Sale in {self.name}"
            stdscr.addstr(0, (width - len(title)) // 2, title, curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)
    
            # Calcular o número de itens que cabem na tela
            max_items = height - 4  # Reservando espaço para título e instruções
            start_idx = offset
            end_idx = min(start_idx + max_items, len(items))
    
            # Exibir os itens visíveis
            for idx in range(start_idx, end_idx):
                item_str = items_to_show[idx]
                # Truncar o item se for muito longo
                if len(item_str) > width - 4:  # Reservando espaço para bordas e seta
                    item_str = item_str[:width - 7] + "..."  # Truncar e adicionar "..."
    
                # Destacar o item selecionado
                if idx == selected_index:
                    stdscr.addstr(2 + idx - start_idx, 2, f"> {item_str}", curses.color_pair(1))
                else:
                    stdscr.addstr(2 + idx - start_idx, 2, f"  {item_str}", curses.color_pair(2))
    
            # Instruções de navegação
            instructions = "Use UP/DOWN to navigate, ENTER to buy, Q to exit."
            stdscr.addstr(height - 2, (width - len(instructions)) // 2, instructions, curses.A_DIM)
            stdscr.refresh()
    
            # Captura a tecla pressionada
            key = stdscr.getch()
    
            if key == curses.KEY_UP and selected_index > 0:
                selected_index -= 1
                if selected_index < offset:
                    offset = selected_index
            elif key == curses.KEY_DOWN and selected_index < len(items) - 1:
                selected_index += 1
                if selected_index >= offset + max_items:
                    offset = selected_index - max_items + 1
            elif key == 10:  # Tecla ENTER
                self.buy_item(selected_index, main_character, stdscr)
                items = self.seller.backpack
                if selected_index >= len(items):
                    selected_index = len(items) - 1
            elif key == ord("q") or key == ord("Q"):
                display_message(stdscr, "Exiting shop inventory.", 1000)
                break
    
    def buy_item(self, selected_index: int, main_character: Hero, stdscr: curses.window) -> None:
        """Handles the purchase of an item."""
        selected_item = self.seller.backpack[selected_index]
        if main_character.gold >= selected_item.value:
            main_character.gold -= selected_item.value
            main_character.backpack.append(selected_item)
            self.seller.backpack.remove(selected_item)
            display_message(stdscr, f"You bought {selected_item.name} for {selected_item.value} gold!", 1000)
        else:
            display_message(stdscr, "You don't have enough gold to buy this item.", 1000)

    def talk_to_seller(self, stdscr: curses.window) -> None:
        """
        Handles interaction with the seller, displaying dialogues in a styled and immersive way.
        """
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Título
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Texto
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Destaque
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)   # Seleção

        # Verifica se o vendedor tem falas
        if not self.seller.speeches:
            display_message(stdscr, "The seller has nothing to say.", 1000, curses.color_pair(2))
            return

        # Usando um atributo para armazenar o índice do último diálogo falado
        if not hasattr(self, "speech_index"):
            self.speech_index = 0  # Inicializa o índice na primeira fala

        while True:
            # Limpa a tela e desenha a borda
            stdscr.clear()
            stdscr.border()

            # Obtém as dimensões da tela
            height, width = stdscr.getmaxyx()

            # Exibe o nome do vendedor centralizado
            seller_title = f"=== {self.seller.name} ==="
            stdscr.addstr(2, (width - len(seller_title)) // 2, seller_title, curses.color_pair(1) | curses.A_BOLD)

            # Exibe a fala atual do vendedor centralizada
            current_speech = self.seller.speeches[self.speech_index]
            stdscr.addstr(height // 2, (width - len(current_speech)) // 2, current_speech, curses.color_pair(2))

            # Exibe instruções para o jogador
            instructions = "Press ENTER to continue, Q to exit."
            stdscr.addstr(height - 2, (width - len(instructions)) // 2, instructions, curses.color_pair(3))

            # Atualiza a tela
            stdscr.refresh()

            # Captura a tecla pressionada
            key = stdscr.getch()

            if key == 10:  # Tecla ENTER
                # Avança para a próxima fala se ainda houverem novas, senão mantém a última
                if self.speech_index < len(self.seller.speeches) - 1:
                    self.speech_index += 1
                else:
                    display_message(stdscr, "That's all the seller has to say.", 1000, curses.color_pair(2))
                    break
            elif key == ord("q") or key == ord("Q"):
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