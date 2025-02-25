from typing import Any, List, Union, Optional, Dict
from quests.quests import Quests, CollectableQuest
from models.item_model import ArmorModel, WeaponModel
from models.abilities_model import BaseAbility
from models.character_class_model import CharacterClass
import curses
from classes.cleric import Cleric
from classes.paladin import Paladin
from classes.rogue import Rogue
from classes.warrior import Warrior
from classes.wizard import Wizard
from collections import Counter
from util.wrap_text import wrap_text

class Hero():
    def __init__(self) -> None:
        self.name: str = "Hero" 
        self.health_points:int = 50
        self.max_hp:int = 50
        self.gold:int = 1000000
        self.backpack:List[Union[WeaponModel, ArmorModel]] = []
        self.abilities: List[BaseAbility] = []
        self.equipments: Dict[str, Optional[Union[ArmorModel, WeaponModel]]] = {
            "torso": None,
            "helmet": None,
            "pants": None,
            "boots": None,
            "weapons": None
        }
        self.character_class:CharacterClass = None
        self.experience:int = 0
        self.next_level_xp:int = 100
        self.attack_points:int = 20
        self.defense_points:int = 20
        self.level:int = 0
        self.critical_hit_chance = 5
        self.resistance_factor = 1
        self.quests: List[Union[Quests, CollectableQuest]] = [] 
        self.concluded_quests: List[Union[Quests, CollectableQuest]] = []
        self.speed = 10 
        self.attack_multiplier = 1
        self.proficiencies = []
        self.extra_actions = 0
        self.dodge_chance = 0
        self.health = 100
        self.last_attack_damage = 0
        self.carry_weight = 50
        self.weight = 0
    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
    
    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.health_points += 10
        self.defense_points += 0.5
        self.attack_points += 0.5
        self.speed *= 1.1
        self.attack_points += self.level + 2
        self.next_level_xp = int(self.next_level_xp * 1.2)
        self.experience = 0
    
        if self.character_class:
            if self.character_class.name == "Fighter":
                self.attack_points += 3
                self.defense_points += 2
                self.health_points += 5
                self.carry_weight += 2
            elif self.character_class.name == "Rogue":
                self.attack_points += 2
                self.critical_hit_chance += 2
                self.speed += 2
                self.carry_weight += 1
            elif self.character_class.name == "Wizard":
                self.resistance_factor += 0.1
            elif self.character_class.name == "Cleric":
                self.defense_points += 1
                self.health_points += 5
                self.carry_weight += 3
            elif self.character_class.name == "Paladin":
                self.attack_points += 2
                self.defense_points += 2
                self.resistance_factor += 0.05
                self.carry_weight += 4
    
    def append_quests(self, quest:Union[Quests, CollectableQuest]):
        self.quests.append(quest)
        
    def init_a_quest(self, quest:Quests):
        self.quests.append(quest)
    
    def conclude_quests(self, quest: Quests):
        if not quest:
            raise ValueError("Quest cannot be None.")
        if quest not in self.quests:
            raise ValueError("Quest is not part of the active quests list.")

        self.gold += quest.gold_given
        self.concluded_quests.append(quest)
        self.quests.remove(quest)
        if self.experience + quest.xp_given < self.next_level_xp:
            self.experience += quest.xp_given
        else:
            remaining_xp = (self.experience + quest.xp_given) - self.next_level_xp
            self.level_up()
            self.experience = remaining_xp

    def equip_item(self, item: Union[ArmorModel, WeaponModel]) -> str:
        if item not in self.backpack:
            return f"Item {item.name} não está na mochila."

        current_equipped_item = None
        weight_to_add = item.weight

        if isinstance(item, WeaponModel):
            current_equipped_item = self.equipments.get("weapon")
        elif isinstance(item, ArmorModel):
            slot = item.type
            current_equipped_item = self.equipments.get(slot)

        if current_equipped_item:
            weight_to_add -= current_equipped_item.weight

        if self.weight + weight_to_add > self.carry_weight:
            return "Você não pode equipar este item, pois ele excede sua capacidade de carga."

        proficiency_bonus = 2 if any(p in self.proficiencies for p in item.proeficiency) else -5

        if isinstance(item, WeaponModel):
            self.attack_points += item.attack_points + proficiency_bonus
            self.last_attack_damage += item.critical_hit_chance
            self.weight += item.weight

            if current_equipped_item:
                self.backpack.append(current_equipped_item)
                self.weight -= current_equipped_item.weight

            self.equipments["weapon"] = item

        elif isinstance(item, ArmorModel):
            slot = item.type
            if slot not in self.equipments:
                return f"Slot {slot} inválido para armadura."

            self.defense_points += item.def_points + proficiency_bonus
            self.weight += item.weight

            if current_equipped_item:
                self.backpack.append(current_equipped_item)
                self.weight -= current_equipped_item.weight

            self.equipments[slot] = item

        self.backpack.remove(item)
        return f"Item {item.name} equipado com sucesso!"

    
    def show_status(self, stdscr: curses.window):
        sections = [
            "Health: {}/{}".format(self.health_points, self.max_hp),
            "Gold: {}".format(self.gold),
            "Experience: {}/{} (Level {})".format(self.experience, self.next_level_xp, self.level),
            "Attack Points: {}".format(self.attack_points),
            "Defense Points: {}".format(self.defense_points),
            "Critical Hit Chance: {}%".format(self.critical_hit_chance),
            "Dodge Chance: {}%".format(self.dodge_chance),
            "Resistance Factor: {}".format(self.resistance_factor),
            "Speed: {}".format(self.speed),
            "Carry Weight: {}/{}".format(self.weight, self.carry_weight),
            "Equipments",
            "Backpack",
            "Abilities",
            "Quests",
            "Proficiencies",
            "Last Attack Damage: {}".format(self.last_attack_damage),
            "Extra Actions: {}".format(self.extra_actions),
        ]

        stdscr.clear()
        current_selection = 0
        top_index = 0

        while True:
            height, width = stdscr.getmaxyx()
            visible_height = height - 1 
            stdscr.clear()

            for i in range(visible_height):
                idx = top_index + i
                if idx >= len(sections):
                    break
                if idx == current_selection:
                    stdscr.addstr(i, 0, f"> {sections[idx]}", curses.A_REVERSE)
                else:
                    stdscr.addstr(i, 0, sections[idx])

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_DOWN: 
                if current_selection < len(sections) - 1:
                    current_selection += 1
                    if current_selection >= top_index + visible_height:
                        top_index += 1
            elif key == curses.KEY_UP: 
                if current_selection > 0:
                    current_selection -= 1
                    if current_selection < top_index:
                        top_index -= 1
            elif key == 10:  
                self.show_section_details(stdscr, sections[current_selection])
            elif key == ord('q'):  
                stdscr.clear()
                stdscr.refresh()
                break

    def show_section(self, stdscr: curses.window, title: str, content: list):
        """Função genérica para exibir uma seção com suporte a rolagem e quebra de linha."""
        top_index = 0
    
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            visible_height = height - 2  # Ajuste para a altura visível
            stdscr.addstr(0, 0, title.center(width), curses.A_BOLD | curses.A_UNDERLINE)
            stdscr.addstr(1, 0, "Use ↑ e ↓ para navegar e 'q' para voltar.\n")
    
            wrapped_content = []
            for line in content:
                wrapped_content.extend(wrap_text(line, width - 2))  # Aplica quebra de linha
    
            for i in range(visible_height):
                idx = top_index + i
                if idx >= len(wrapped_content):
                    break
                stdscr.addstr(i + 2, 0, wrapped_content[idx])
    
            stdscr.refresh()
            key = stdscr.getch()
    
            if key == curses.KEY_DOWN:
                if top_index + visible_height < len(wrapped_content):
                    top_index += 1
            elif key == curses.KEY_UP:
                if top_index > 0:
                    top_index -= 1
            elif key == ord('q'):
                break

    def show_inventory(self, stdscr: curses.window):
        """Mostra o inventário do jogador com navegação e seleção."""
        current_row = 0

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            visible_height = height - 3 

            stdscr.addstr(0, 0, "Inventário".center(width), curses.A_BOLD | curses.A_UNDERLINE)
            stdscr.addstr(1, 0, "Use ↑ e ↓ para navegar, Enter para selecionar, 'q' para sair.\n")

            for i in range(visible_height):
                idx = current_row - (current_row % visible_height) + i
                if idx >= len(self.backpack):
                    break
                if idx == current_row:
                    stdscr.addstr(i + 2, 0, f"> {self.backpack[idx]}", curses.A_REVERSE)
                else:
                    stdscr.addstr(i + 2, 0, f"  {self.backpack[idx]}")

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_DOWN and current_row < len(self.backpack) - 1:
                current_row += 1
            elif key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == ord('\n') and len(self.backpack) > 0:
                selected_item = self.backpack[current_row]
                result = self.equip_item(selected_item)
                self.show_section(stdscr, "Item Selecionado", [result, "Pressione 'q' para voltar."])
            elif key == ord('q'):
                stdscr.clear()
                stdscr.refresh()
                break


    def show_section_details(self, stdscr: curses.window, section: str):
        """Mostra os detalhes de uma seção."""
        if section == "Backpack":
            content = ["Conteúdo da Mochila:"]
            if self.backpack:
                item_counts = Counter(self.backpack)
                content.extend(f"- {quantity}x {item.name} (Valor: {item.value}, Peso: {item.weight})"
                               for item, quantity in item_counts.items())
            else:
                content.append("- Your backpack is empty.")
        elif section == "Equipments":
            content = ["Equipments:"]
            content.extend(f"{item_type.capitalize()}: {item if item else 'None'}" for item_type, item in self.equipments.items())
        elif section == "Abilities":
            content = ["Skills:"]
            content.extend(f"- {ability}" for ability in self.abilities)
        elif section == "Quests":
            content = ["Active quests:"]
            content.extend(f"- {quest}" for quest in self.quests)
            content.append("Concluded quests:")
            content.extend(f"- {quest}" for quest in self.concluded_quests)
        elif section == "Proficiencies":
            content = ["Proficiencies:"]
            content.extend(f"- {proficiency}" for proficiency in self.proficiencies)
        else:
            content = [f" {section}."]
        self.show_section(stdscr, section, content)


    def choose_character_class(self, stdscr: curses.window):
        classes = ["Fighter", "Rogue", "Wizard", "Cleric", "Paladin"]
        current_row = 0

        while True:
            stdscr.clear()
            stdscr.addstr("Use ↑ and ↓ to navigate, Enter to select a class, and 'q' to quit.\n\n")

            for idx, character_class in enumerate(classes):
                if idx == current_row:
                    stdscr.addstr(f"> {character_class}\n", curses.A_REVERSE)
                else:
                    stdscr.addstr(f"  {character_class}\n")

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(classes) - 1:
                current_row += 1
            elif key == ord('\n'): 
                selected_class = classes[current_row]
                break
            elif key == ord('q'):  
                return "Defaulting to Fighter."

            stdscr.refresh()

        if selected_class == "Fighter":
            self.character_class = Warrior()
        elif selected_class == "Rogue":
            self.character_class = Rogue()
        elif selected_class == "Wizard":
            self.character_class = Wizard()
        elif selected_class == "Cleric":
            self.character_class = Cleric()
        elif selected_class == "Paladin":
            self.character_class = Paladin()

        self.apply_class(self.character_class)

        return f"Class {selected_class} chosen successfully!"
        
        
    
    def apply_class(self, character_class: CharacterClass):
        """Applies a character class to the hero."""
        self.health += character_class.health
        self.max_hp += character_class.health
        self.proficiencies.extend(character_class.proficiencies)
        self.abilities = character_class.abilities
        self.primary_stat = character_class.primary_stat
        self.spell_slots = character_class.spell_slots 
    
    def add_to_inventory(self, item):
        self.backpack.append(item)
        self.weight += item.weight

    def remove_items_from_backpack(self, items_to_be_collected):
        for item, quantity in items_to_be_collected:
            available_quantity = sum(1 for i in self.backpack if i == item)
            if available_quantity < quantity:
                raise ValueError(f"Not enough {item.name} in the backpack. Needed {quantity}, found {available_quantity}.")

        for item, quantity in items_to_be_collected:
            count = 0
            for i in range(len(self.backpack) - 1, -1, -1):  
                if self.backpack[i] == item:
                    self.backpack.pop(i)
                    self.weight -= item.weight
                    count += 1
                    if count == quantity:  
                        break
    
    def find_quest_by_id(self, quest_id: int):
        return next((quest for quest in self.quests if quest.id == quest_id), None)
