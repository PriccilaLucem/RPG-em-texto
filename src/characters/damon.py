import curses
from models.npc_model import Character_with_a_quest_model
from util.display_message import draw_menu, draw_menu_with_history
from quests.main_quests import prismeer_owl_bear_quest
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
        options = ["Continue", "Ask more", "Leave"]
        while True:
            response = """Damon
                We thought the caves were abandoned...
                But something's changed. The owlbears... they're not natural.
                Bigger. Angrier. Eyes glowing like hot coals.
                My brothers went to investigate three days ago.
                Haven't returned.
                We should go there to find the
            """
            
            draw_menu_with_history(self.stdscr, "=== Damon - Veteran Guardsman ===", response, options, index)
            key = self.stdscr.getch()
            
            if key == 10 and index == 2:  
                break

    def _show_reward_info(self):
        index = 0
        options = ["Continue", "Ask about the blade", "Leave"]
        while True:
            response = """
                The town coffers are light, but...
                Rescue my brothers and I'll give you
                the ancestral blade from our family armory.
                It's seen more battles than I have winters.            
            """
            draw_menu_with_history(self.stdscr, "=== Reward Information ===", response, options, index)
            key = self.stdscr.getch()
            if key == 10:
                ...  # TODO

    def _show_cave_information(self):
        options = ["Learn more", "Back"]
        index = 0
        while True:
            response = """
                Ancient dwarven mining tunnels
                Abandoned after a cave-in century ago
                Recent reports of:
                - Strange lights
                - Animal mutations
                - Disappearing travele
            """
            
            draw_menu_with_history(self.stdscr, "The Howling Caverns", response, options, index)
            key = self.stdscr.getch()
            if key == 10:
                ...    

    def _handle_quest_completion(self, main_character):
        response = """You brought them back...
            *he stares at his brothers' wrapped bodies*
            This wasn't the homecoming I...
            *he hands you a rusted greatsword*
            Take it. They'd want you to have 
            """
        options = ["Accept sword", "Offer condolences", "Kill Damon", "Run"]
        index = 0
        while True:
            draw_menu_with_history(self.stdscr, "=== Quest Complete ===", response, options, index)
            #TODO

    def talk_to_damon(self, main_character: 'MainCharacter'):
        while True:
            options = self._show_initial_options()
            index = 0 
            
            key = None
            while key != 10:
                draw_menu(self.stdscr, "=== Damon - Veteran Guardsman ===", options, index)
                key = self.stdscr.getch()
                if key == curses.KEY_UP:
                    index = max(0, index-1)
                elif key == curses.KEY_DOWN:
                    index = min(len(options)-1, index+1)
            
            if key == 10:
                selected = options[index]
                
                if selected == "What happened to your brothers?":
                    self._handle_brothers_dialogue()
                elif selected == "Tell me about the Owlbear caves":
                    self._show_cave_information()
                elif selected == "What's in this for me?":
                    self._show_reward_info()
                elif selected.startswith("I'm working on"):
                    self._handle_quest_in_progress(main_character)
                elif selected == "Leave conversation":
                    break

    def _show_initial_options(self):
        options = [
            "What happened to your brothers?",
            "Tell me about the Owlbear caves", 
            "What's in this for me?",
            "Leave conversation"
        ]
        
        if self.quest_accepted and not self.quest_complete:
            options.insert(0, "I'm working on rescuing your brothers")
        
        return options

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
