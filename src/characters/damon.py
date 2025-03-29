import curses
from models.npc_model import Character_with_a_quest_model
from util.display_message import draw_menu, draw_menu_with_history
from quests.main_quests import prismeer_owl_bear_quest
from history.mine_history import MineHistory
from history.brothers_history import BrotherDialogue
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from characters.main_character import MainCharacter


class Damon(Character_with_a_quest_model):
    def __init__(self, stdscr: curses.window):
        super().__init__(
            name="Damon",
            speeches=[
                "You finally came... I was beginning to think you'd abandoned us.",
                "The howls from the caves grow louder each night...",
                "My brothers... they were exploring the mine witch OwlBear have appeared!"
            ],
            quest=prismeer_owl_bear_quest
        )
        self.stdscr = stdscr
        self.quest_accepted = False
        self.quest_complete = False

    def _handle_brothers_dialogue(self):
        index = 0
        options = ["Ask more", "Leave"]

        while True:
            response = BrotherDialogue.initial_dialogue()
            draw_menu_with_history(self.stdscr, "=== Damon - Veteran Guardsman ===", response, options, index)
            
            key = self.stdscr.getch()
            
            if key in (curses.KEY_UP, curses.KEY_DOWN):
                index = (index + 1) % len(options)
            elif key == 10:  # Enter key
                if options[index] == "Ask more":
                    self._handle_ask_more_dialogue()
                elif options[index] == "Leave":
                    break

    def _handle_ask_more_dialogue(self):
        ask_index = 0
        ask_options = [
            "About Jorik (the elder brother)",
            "About Baldric (the younger brother)",
            "About their last mission",
            "Back"
        ]
        
        while True:
            ask_response = BrotherDialogue.ask_more_dialogue()
            draw_menu_with_history(self.stdscr, "=== The Lost Brothers ===", ask_response, ask_options, ask_index)
            
            ask_key = self.stdscr.getch()
            
            if ask_key == curses.KEY_UP:
                ask_index = max(0, ask_index - 1)
            elif ask_key == curses.KEY_DOWN:
                ask_index = min(len(ask_options) - 1, ask_index + 1)
            elif ask_key == 10:  # Enter
                if ask_options[ask_index] == "About Jorik (the elder brother)":
                    self._show_jorik_details()
                elif ask_options[ask_index] == "About Baldric (the younger brother)":
                    self._show_baldric_details()
                elif ask_options[ask_index] == "About their last mission":
                    self._last_mission_details()
                elif ask_options[ask_index] == "Back":
                    break

    def _last_mission_details(self):
        last_mission_response = BrotherDialogue.last_mission_details()
        draw_menu_with_history(self.stdscr, "=== Last Mission ===", last_mission_response, ["Continue"], 0)
        self.stdscr.getch()

    def _show_jorik_details(self):
        detail_response = BrotherDialogue.jorik_details()
        draw_menu_with_history(self.stdscr, "=== Jorik Ironoak ===", detail_response, ["Continue"], 0)
        self.stdscr.getch()

    def _show_baldric_details(self):
        detail_response = BrotherDialogue.baldric_details()
        draw_menu_with_history(self.stdscr, "=== Baldric the Bright ===", detail_response, ["Continue"], 0)
        self.stdscr.getch()
    
    def talk_to_damon(self, main_character: 'MainCharacter'):
        while True:
            options = self._show_initial_options()
            index = 0
            key = None
            
            while key != 10:
                draw_menu(self.stdscr, "=== Damon - Veteran Guardsman ===", options, index)
                key = self.stdscr.getch()
                if key == curses.KEY_UP:
                    index = max(0, index - 1)
                elif key == curses.KEY_DOWN:
                    index = min(len(options) - 1, index + 1)
            
            selected = options[index]
            if selected == "What happened to your brothers?":
                self._handle_brothers_dialogue()
            if selected == "Ask about the cave":
                self._show_cave_information()
            elif selected == "Leave conversation":
                break
    
    def _show_initial_options(self):
        options = [
            "What happened to your brothers?",
            "Ask about the cave",
            "Leave conversation",
        ]
        if self.quest_accepted and not self.quest_complete:
            options.insert(0, "I'm working on rescuing your brothers")
        return options

    def _show_cave_information(self):
            """Show cave info with loop"""
            options = ["Learn more", "Back"]
            history = MineHistory.show_cave_information()
            index = 0
            while True:
                draw_menu_with_history(self.stdscr,"=== The ancient Cave ===", history, options, index)
                
                key = self.stdscr.getch()
                
                if key == curses.KEY_UP:
                    index = max(0, index-1)
                elif key == curses.KEY_DOWN:
                        index = min(len(options)-1, index+1)
                elif key == 10:
                    if options[index].startswith("Learn more"):
                        self._show_cave_history()
                    elif options[index].startswith("Back"):
                        break
    
    def _show_cave_history(self):
        options = ["Dwarven builders", "Mining operations", "The Great Collapse", "Recent events", "Back"]
        index = 0
        while True:
            draw_menu(self.stdscr, "=== Mine History ===", options, index)
            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                index = max(0, index - 1)
            elif key == curses.KEY_DOWN:
                index = min(len(options) - 1, index + 1)
            elif key == 10:
                if options[index] == "Dwarven builders":
                    detail = MineHistory.dwarven_builders()
                    draw_menu_with_history(self.stdscr, "=== Builders ===", detail, ["Continue"], 0)
                    self.stdscr.getch()
                        
                elif options[index] == "Mining operations":
                    detail = MineHistory.mining_operations()
                    draw_menu_with_history(self.stdscr, "=== Operations ===", detail, ["Continue"], 0)
                    self.stdscr.getch()
                        
                elif options[index] == "The Great Collapse":
                    detail = MineHistory.the_great_collapse()
                    draw_menu_with_history(self.stdscr, "=== Collapse ===", detail, ["Continue"], 0)
                    self.stdscr.getch()
                        
                elif options[index] == "Recent events":
                    detail = MineHistory.recent_events()
                    draw_menu_with_history(self.stdscr, "=== Recent Times ===", detail, ["Continue"], 0)
                    self.stdscr.getch()
                        
                elif options[index] == "Back":
                    break


    @classmethod
    def from_dict(cls, data, stdsc):
        damon = cls(stdsc)
        damon.speeches = data["speeches"]
        damon.name = "Damon"
        damon.quest = data["quest"]
        damon.quest_accepted = data["quest_accepted"]
        damon.quest_complete = data["quest_complete"]
        return damon

    def to_dict(self):
        data = super().to_dict()
        data["quest_accepted"] = self.quest_accepted
        data["quest_complete"] = self.quest_complete
        return data
    
