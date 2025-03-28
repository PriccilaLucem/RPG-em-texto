import curses
from models.bar_model import Bar
from characters.main_character import MainCharacter
from resources.prismeer.foods import french_fries, creaft_burger, chiken_wings, beer
from resources.prismeer.people import barmaid, drunkard, shady_dealer, guard, mercenary, stranger
from models.npc_model import Seller_model, Bardo, Character_with_a_quest_model
from history.bardo_history import the_ballad_of_prismeer_and_north
from util.display_message import draw_menu, display_message, draw_menu_with_history

class PrismeerBar(Bar):
    def __init__(self):
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
    
    def bar_menu(self, stdscr: curses.window, main_character: MainCharacter):
        """Main bar menu navigation"""
        options = [
            "Talk to Patrons",
            "Order from Bartender",
            "Listen to the Bard",
            "Leave the Bar"
        ]
        index = 0
        title = f"=== {self.name} ==="

        while True:
            draw_menu(stdscr, title, options, index)
            key = stdscr.getch()
            
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10:  # Enter key
                if options[index] == "Talk to Patrons":
                    self.choose_patron(stdscr, main_character)
                elif options[index] == "Order from Bartender":
                    self.order_from_bartender(stdscr, main_character)
                elif options[index] == "Listen to the Bard":
                    self.talk_to_bard(stdscr, main_character)
                elif options[index] == "Leave the Bar":
                    display_message(stdscr, "You exit the bar, stepping back into the bustling streets.")
                    break

    def choose_patron(self, stdscr: curses.window, main_character: MainCharacter):
        """Menu to select which NPC to interact with"""
        options = [npc.name for npc in self.people] + ["Back to Bar"]
        index = 0
        title = "=== Who do you approach? ==="
        speech_index = 0

        while True:
            draw_menu(stdscr, title, options, index)
            key = stdscr.getch()
            
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
                    self.talk_to_npc(stdscr, main_character)

    def talk_to_npc(self, stdscr: curses.window, main_character: MainCharacter):
        """Handle conversation with selected NPC"""
        if not self.current_npc:
            return

        options = ["Keep Talking", "Ask About Quest", "Leave Conversation"]
        index = 0
        title = f"=== {self.current_npc.name} ==="
        speech_index = 0
        quest_offered = False

        while True:
            # Special case for quest-giving NPCs
            if isinstance(self.current_npc, Character_with_a_quest_model) and not quest_offered:
                options = ["Keep Talking", "Ask About Quest", "Leave Conversation"]
            else:
                options = ["Keep Talking", "Leave Conversation"]

            draw_menu(stdscr, title, options, index)
            key = stdscr.getch()
            
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10: 
                if options[index] == "Keep Talking":
                    display_message(stdscr,f"{self.current_npc.name}: {self.current_npc.speech(speech_index)}", 2000)
                    speech_index = (speech_index + 1) % len(self.current_npc.speeches)
                elif options[index] == "Ask About Quest" and isinstance(self.current_npc, Character_with_a_quest_model):
                    self.handle_quest(stdscr, main_character)
                    quest_offered = True
                elif options[index] == "Leave Conversation":
                    break

    def handle_quest(self, stdscr: curses.window, main_character: MainCharacter):
        """Display quest details and handle acceptance"""
        if not isinstance(self.current_npc, Character_with_a_quest_model):
            return

        quest = self.current_npc.quest
        title = f"=== {quest.mission} ==="
        
        # Format quest details
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
            draw_menu_with_history(stdscr, title, "\n".join(details), options, index)
            key = stdscr.getch()
            
            if key == curses.KEY_UP or key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10:  # Enter key
                if options[index] == "Accept Quest":
                    main_character.append_quests(quest)
                    display_message(stdscr, f"Quest accepted: {quest.mission}", 2000)
                break

    def order_from_bartender(self, stdscr: curses.window, main_character: MainCharacter):
        """Handle ordering food/drinks from bartender"""
        options = [f"{item.name} - {item.value} gold" for item in self.food] + ["Back"]
        index = 0
        title = "=== Bartender's Menu ==="

        while True:
            draw_menu(stdscr, title, options, index)
            key = stdscr.getch()
            
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
                        display_message(stdscr, f"You bought {selected_item.name}!", 1500)
                    else:
                        display_message(stdscr, "Not enough gold!", 1500)

    def talk_to_bard(self, stdscr: curses.window, main_character: MainCharacter):
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
            draw_menu(stdscr, title, options, index)
            key = stdscr.getch()
            
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == 10:  # Enter key
                if options[index] == "Chat with Bard":
                    display_message(stdscr, f"{self.bardo.name} {self.bardo.speech(speech_index)}", 2000)
                    speech_index = (speech_index + 1) % len(self.bardo.speeches)
                elif options[index].startswith("Pay"):
                    if main_character.gold >= self.bardo.price:
                        main_character.gold -= self.bardo.price
                        self.listen_to_song(stdscr)
                    else:
                        display_message(stdscr, "Not enough gold!", 2000)
                elif options[index] == "Back to Bar":
                    break

    def listen_to_song(self, stdscr: curses.window):
        """Display the bard's song/poem"""
        title = "=== The Ballad of Prismeer and North ==="
        options = ["Continue"]
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)

        while True:
            draw_menu_with_history(stdscr, title, self.bardo.history, options, 0, curses.color_pair(10))
            key = stdscr.getch()
            if key == 10:
                break