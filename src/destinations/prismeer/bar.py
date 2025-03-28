import curses
from models.bar_model import Bar
from characters.main_character import MainCharacter
from characters.damon import Damon
from resources.prismeer.foods import french_fries, creaft_burger, chiken_wings, beer
from resources.prismeer.people import barmaid, drunkard, shady_dealer, guard, mercenary, stranger
from models.npc_model import Seller_model, Bardo, Character_with_a_quest_model
from history.bardo_history import the_ballad_of_prismeer_and_north
from history.damon_history import enter_the_bar_with_damon
from util.display_message import draw_menu, display_message, draw_menu_with_history
from history.damon_history import enter_the_bar_with_damon


class PrismeerBar(Bar):
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.name = "Might & Magic Bar"
        self.food = [french_fries, creaft_burger, chiken_wings, beer]
        self.bartender = Seller_model(
            name="Oswaldo",
            speeches=[
                "Order something or get out!",
                "HEY YOU, what are you staring at?",
                "You have nothing to do with me just buy something"
            ],
            backpack=self.food
        )
        
        self.people = [barmaid, drunkard, shady_dealer, guard, mercenary, stranger]
        self.current_npc = None
        
        self.bardo = Bardo(
            name="Mel",
            speeches=[
                "For just a coin, I'll sing your story!",
                "♪~The ale here flows like golden rain~♪",
                "My lute and I have traveled far... farther than my money.",
                "Request a song? Make it worth my while."
            ],
            price=20,
            history=the_ballad_of_prismeer_and_north()
        )
        
        super().__init__(self.food, self.people, self.bartender, self.bardo)
    
    def bar_menu(self, main_character: MainCharacter, damon:Character_with_a_quest_model = None):
        """Main bar menu navigation"""
        options = [
            "Talk to Patrons",
            "Talk to Bartender",
            "Listen to the Bard",
            "Leave the Bar"
        ]
        if damon:
            index = 0
            options = ["Talk to Damon"]
            title = f"=== Entering the {self.name} ==="
            while True:
                draw_menu_with_history(self.stdscr, title, enter_the_bar_with_damon(), options, index)
                if self.stdscr.getch() == 10:
                    break
            self._entering_the_bar_with_damon(main_character, damon)
            
        
        index = 0
        title = f"=== {self.name} ==="
        while True: 
            draw_menu(self.stdscr, title, options, index)
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10:
                if options[index] == "Talk to Patrons":
                    self.choose_patron(self.stdscr, main_character)
                elif options[index] == "Talk to Bartender":
                    self.bartender_menu(self.stdscr, main_character)
                elif options[index] == "Listen to the Bard":
                    self.talk_to_bard(self.stdscr, main_character)
                elif options[index] == "Leave the Bar":
                    display_message(self.stdscr, "You exit the bar, stepping back into the bustling streets.")
                    break

    def choose_patron(self, main_character: MainCharacter):
        """Menu to select which NPC to interact with"""
        options = [npc.name for npc in self.people] + ["Back to Bar"]
        index = 0
        title = "=== Who do you approach? ==="

        while True:
            draw_menu(self.stdscr, title, options, index)
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10:  # Enter key
                if options[index] == "Back to Bar":
                    break
                else:
                    selected_npc = self.people[index]
                    self.current_npc = selected_npc
                    self.talk_to_npc(self.stdscr, main_character)

    def talk_to_npc(self,main_character: MainCharacter):
        """Handle conversation with selected NPC"""
        if not self.current_npc:
            return

        index = 0
        title = f"=== {self.current_npc.name} ==="
        speech_index = 0
        all_speeches_heard = False
        quest_available = isinstance(self.current_npc, Character_with_a_quest_model)

        while True:
            current_options = ["Keep Talking"]
            
            if (quest_available and 
                all_speeches_heard and 
                isinstance(self.current_npc, Character_with_a_quest_model)):
                current_options.append("Ask About Quest")
                
            current_options.append("Leave Conversation")

            draw_menu(self.stdscr, title, current_options, index)
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                index = (index - 1) % len(current_options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(current_options)
            elif key == 10:  # Enter key
                selected_option = current_options[index]
                
                if selected_option == "Keep Talking":
                    display_message(
                        self.stdscr,
                        f"{self.current_npc.name}: {self.current_npc.speech(speech_index)}",
                        2000
                    )
                    speech_index = (speech_index + 1) % len(self.current_npc.speeches)
                    
                    if speech_index == 0:
                        all_speeches_heard = True
                        
                elif selected_option == "Ask About Quest":
                    self.handle_quest(self.stdscr, main_character)
                    quest_available = False  
                    
                elif selected_option == "Leave Conversation":
                    break

    def handle_quest(self, main_character: MainCharacter):
        """Display quest details and handle acceptance"""
        if not isinstance(self.current_npc, Character_with_a_quest_model):
            return

        quest = self.current_npc.quest
        title = f"=== {quest.mission} ==="
        
        details = [
            quest.description,
            "",
            f"Reward: {quest.gold_given} gold",
            f"Difficulty: {'★' * quest.difficult_stars}",
            "",
            quest.additional_info.get("location", ""),
            quest.additional_info.get("special_condition", "")
        ]
        
        options = ["Accept Quest", "Decline"]
        index = 0

        while True:
            draw_menu_with_history(self.stdscr, title, "\n".join(details), options, index)
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP or key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10:  # Enter key
                if options[index] == "Accept Quest":
                    main_character.append_quests(quest)
                    display_message(self.stdscr, f"Quest accepted: {quest.mission}", 2000)
                break
    
    def bartender_menu(self, main_character: MainCharacter):
        display_message(self.stdscr, "What do you want??", 2000)
        options = [
            "Talk to bartender",
            "Buy something",
            "Back to bar"
        ]
        index = 0 
        title = f"==== {self.bartender.name} ==="
        bar_speech_index = 0 
        while True:
            draw_menu(self.stdscr, title, options, index)
            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10:  # Enter key
                if options[index].startswith("Back to bar"):
                    break
                elif options[index].startswith("Talk to bartender"):
                    display_message(self.stdscr, f"{self.bartender.name}:  {self.bartender.speech(bar_speech_index)}")
                    bar_speech_index += 1
                elif options[index].startswith("Buy something"):
                    self.order_from_bartender(main_character)


    def order_from_bartender(self, main_character: MainCharacter):
        """Handle ordering food/drinks from bartender"""
        options = [f"{item.name} - {item.value} gold" for item in self.food] + ["Back"]
        index = 0
        title = "=== Bartender's Menu ==="

        while True:
            draw_menu(self.stdscr, title, options, index)
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10:  # Enter key
                if options[index] == "Back":
                    break
                else:
                    selected_item = self.food[index]
                    if main_character.gold >= selected_item.value:
                        main_character.gold -= selected_item.value
                        main_character.add_to_inventory(selected_item)
                        display_message(self.stdscr, f"You bought {selected_item.name}!", 1500)
                    else:
                        display_message(self.stdscr, "Not enough gold!", 1500)

    def talk_to_bard(self, main_character: MainCharacter):
        """Handle bard interaction"""
        options = [
            "Chat with Bard",
            f"Pay {self.bardo.price} gold for a song",
            "Back to Bar"
        ]
        index = 0
        title = f"=== {self.bardo.name} the Bard ==="
        speech_index = 0

        while True:
            draw_menu(self.stdscr, title, options, index)
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10:  
                if options[index] == "Chat with Bard":
                    display_message(self.stdscr, f"{self.bardo.name} {self.bardo.speech(speech_index)}", 2000)
                    speech_index = (speech_index + 1) % len(self.bardo.speeches)
                elif options[index].startswith("Pay"):
                    if main_character.gold >= self.bardo.price:
                        main_character.gold -= self.bardo.price
                        self.listen_to_song(self.stdscr)
                    else:
                        display_message(self.stdscr, "Not enough gold!", 2000)
                elif options[index] == "Back to Bar":
                    break

    def listen_to_song(self):
        """Display the bard's song/poem"""
        title = "=== The Ballad of Prismeer and North ==="
        options = ["Continue"]
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)

        while True:
            draw_menu_with_history(self.stdscr, title, self.bardo.history, options, 0, curses.color_pair(10))
            key = self.stdscr.getch()
            if key == 10:
                break


    def _entering_the_bar_with_damon(self, main_character: MainCharacter, damon: Damon):
        while True:
            damon.talk_to_damon(main_character)
            break
    
    def to_dict(self) -> dict:
        """Convert the PrismeerBar instance to a dictionary"""
        return {
            'name': self.name,
            'food': [item.to_dict() for item in self.food],
            'bartender': self.bartender.to_dict(),
            'people': [person.to_dict() for person in self.people],
            'bardo': self.bardo.to_dict(),
            'current_npc': self.current_npc.to_dict() if self.current_npc else None
        }
    @classmethod
    def from_dict(cls, data: dict, stdscr) -> 'PrismeerBar':
        from models.item_model import ItemModel
        from models.npc_model import (
            Seller_model, 
            Bardo, 
            Character_model, 
            Character_with_a_quest_model
        )
        
        bar = cls(stdscr)
        bar.name = data['name']
        
        bar.food = [ItemModel.from_dict(item_data) for item_data in data['food']]
        
        bar.bartender = Seller_model.from_dict(data['bartender'])
        bar.bartender = bar.food  
        
        bar.people = []
        for person_data in data['people']:
            if 'quest' in person_data:
                person = Character_with_a_quest_model.from_dict(person_data)
            else:  
                person = Character_model.from_dict(person_data)
            bar.people.append(person)
        
        bar.bardo = Bardo.from_dict(data['bardo'])
        
        if data['current_npc']:
            current_npc_data = data['current_npc']
            if 'quest' in current_npc_data:
                bar.current_npc = Character_with_a_quest_model.from_dict(current_npc_data)
            else:
                bar.current_npc = Character_model.from_dict(current_npc_data)
        
        return bar