from typing import Dict
from models.shop_model import Shop_model
from models.character_model import Character_model
from models.character_with_a_quest_model import Character_with_a_quest_model
from destinations.prismeer.items import generate_armor_from_prismeer_seller, generate_weapon_from_prismeer_seller
from characters.hero import Hero
from typing import List, Union
from quests import prismeer_owl_bear_quest, prismeer_blacksmith_quest
import curses
from util.display_message import display_message, draw_menu

class Comercial_center:
    def __init__(self, stdscr) -> None:
        self.armor_shop = Shop_model("Two Brothers Armory", "Baron",[
            "Welcome to Two Brothers Armory, what would you like to buy?",
            "We have a great Amory since the foundation of Prissmer",
            "Take a look in my armory, feel at home"], generate_armor_from_prismeer_seller(), stdscr)

        self.weapon_shop = Shop_model("Brotherhood of the swords", "Chimaru", [
            "Yo, here we sell swords, only swords. We don't like other weapons",
            "We here opened as a bar, but now we sell swords, because swords are the best",
            "Are you gonna buy or just taking a look?"
        ], generate_weapon_from_prismeer_seller(),stdscr)

        self.npcs: List[Union[Character_model, Character_with_a_quest_model]] = [
            Character_model("Afrac", ["Hello There i'm Afrac, nice to meet you"]),
            Character_model("Osvaldo", ["Do you have any vodka? I want to drink"]),
            Character_with_a_quest_model(name="Damon", speeches=[
                "Hero! Hero! Please you have to help my brothers... They tried to take the treasure of OwBear and now they are trapped in his cave!",
                "Thank you hero!"], quest=prismeer_owl_bear_quest),
            Character_with_a_quest_model(name="Walver", speeches=[
                "You are not ready!",
                "Please help me find some ores",
                "Thank you, now you can use my forge"
            ], quest=prismeer_blacksmith_quest)
        ]

    @classmethod
    def from_dict(cls, data: Dict):
        comercial_center = cls()
        comercial_center.armor_shop = Shop_model.from_dict(data['armor_shop'])
        comercial_center.weapon_shop = Shop_model.from_dict(data['weapon_shop'])
        comercial_center.npcs = [
            Character_with_a_quest_model.from_dict(npc_data) if 'quest' in npc_data and npc_data['quest'] is not None else Character_model.from_dict(npc_data)
            for npc_data in data['npcs']
        ]
        return comercial_center

    
    def to_dict(self) -> Dict:
        return {
            "armor_shop": self.armor_shop.to_dict(),
            "weapon_shop": self.weapon_shop.to_dict(),
            "npcs": [npc.to_dict() for npc in self.npcs] 
        }

    def talk_to_npc(self, key: int, main_character: Hero):
        npc_to_talk = self.npcs[key - 1]
        if any(quest.id == 1 for quest in main_character.concluded_quests) and key == 3:
            return npc_to_talk.speech(1)
        if key == 4:
            if any(quest.id == 2 for quest in main_character.concluded_quests):
                return npc_to_talk.speech(2)   
            elif main_character.character_class is None:
                return npc_to_talk.speech(0)
            else:
                return npc_to_talk.speech(1)
        else:
            return npc_to_talk.speech(0)

    def append_npc_quest(self, main_character: Hero, npc_key: int = None):
        if npc_key is not None:
            npc = self.npcs[npc_key - 1]
            if isinstance(npc, Character_with_a_quest_model) and npc.quest is not None:
                main_character.append_quests(npc.quest)
                npc.quest = None
    
    def talk_to_blacksmith(self, stdscr, main_character: Hero):
        
        blacksmith = next(npc for npc in self.npcs if npc.name == "Walver")

        blacksmith_dialogue = [
            "Walver: You are not ready!",
            "Walver: Please help me find some ores.",
            "Walver: Thank you, now you can use my forge.",
        ]

        # Exibe o diálogo inicial
        if not any(quest.id == 2 for quest in main_character.quests):
            display_message(stdscr, blacksmith_dialogue[0], 2000, curses.color_pair(1))  # Usa color_pair(2) para o texto
            return

        curses.napms(500)

        # Opções do menu
        options = [
            "Ask about quests",
            "Deliver collected items",
            "Return to city center",
        ]
        selected_index = 0

        while True:
            
            draw_menu(stdscr, "Blacksmith's Forge", options, selected_index)

            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif key == 10:  # Tecla ENTER
                if selected_index == 0:  # Perguntar sobre missões
                    self.handle_blacksmith_quest_offer(stdscr, main_character, blacksmith)
                elif selected_index == 1:  # Entregar itens coletados
                    self.handle_blacksmith_item_delivery(stdscr, main_character, blacksmith)
                elif selected_index == 2:  # Retornar ao centro da cidade
                    break

            
    def handle_blacksmith_quest_offer(self, stdscr, main_character, blacksmith):
        """
        Oferece a missão do ferreiro ao jogador.
        """
        if isinstance(blacksmith, Character_with_a_quest_model) and blacksmith.quest is not None:
            # Exibe a oferta de missão
            display_message(stdscr, "Walver: Please help me find some ores.", 2000, curses.color_pair(2))

            # Opções de resposta
            options = ["Y - Accept the quest", "N - Deny the quest"]
            selected_index = 0

            while True:
                draw_menu(stdscr, "Quest Offer", options, selected_index)
                key = stdscr.getch()

                if key == curses.KEY_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif key == curses.KEY_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif key == 10:  # Tecla ENTER
                    if selected_index == 0:  # Aceitar missão
                        main_character.append_quests(blacksmith.quest)
                        blacksmith.quest = None
                        display_message(stdscr, "Quest Accepted!", 1500, curses.color_pair(2))
                    else:  # Recusar missão
                        display_message(stdscr, "Quest Denied.", 1500, curses.color_pair(2))
                    break
                elif key == 27:  # Tecla ESC
                    break
        else:
            display_message(stdscr, "Walver: I have no quests for you right now.", 2000, curses.color_pair(2))
        
                    