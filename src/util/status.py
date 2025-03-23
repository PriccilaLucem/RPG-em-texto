import curses
from util.display_message import draw_menu
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from characters.main_character import MainCharacter
from collections import Counter

def init_colors():
    """Initialize color pairs for curses."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

def show_status(main_character: "MainCharacter", stdscr: curses.window):
    init_colors()  # Initialize colors
    sections = [
        "Health: {}/{}".format(main_character.health_points, main_character.max_hp),
        "Gold: {}".format(main_character.gold),
        "Experience: {}/{} (Level {})".format(main_character.experience, main_character.next_level_xp, main_character.level),
        "Attack Points: {}".format(main_character.attack_points),
        "Defense Points: {}".format(main_character.defense_points),
        "Critical Hit Chance: {}%".format(main_character.critical_hit_chance),
        "Dodge Chance: {}%".format(main_character.dodge_chance),
        "Resistance Factor: {}".format(main_character.resistance_factor),
        "Speed: {}".format(main_character.speed),
        "Carry Weight: {}/{}".format(main_character.weight, main_character.carry_weight),
        "Equipments",
        "Backpack",
        "Abilities",
        "Quests",
        "Proficiencies",
        "Last Attack Damage: {}".format(main_character.last_attack_damage),
        "Extra Actions: {}".format(main_character.extra_actions),
    ]

    current_selection = 0
    top_index = 0

    while True:
        height, width = stdscr.getmaxyx()
        visible_height = height - 2  # Reserve space for instructions

        # Clear screen and draw title
        stdscr.clear()
        draw_menu(stdscr, "=== Status ===", sections, current_selection, "Use ↑/↓ to navigate, ENTER to select, 'q' to quit")

        stdscr.refresh()

        # Capture user input
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
        elif key == 10:  # ENTER key
            show_section_details(main_character, stdscr, sections[current_selection])
        elif key == ord('q'):
            break

def show_section_details(main_character: "MainCharacter", stdscr: curses.window, section: str):
    """Display details of a selected section."""
    if section == "Backpack":
        content = ["Backpack Contents:"]
        if main_character.backpack:
            item_counts = Counter(main_character.backpack)
            content.extend(f"- {quantity}x {item.name} (Value: {item.value}, Weight: {item.weight})"
                           for item, quantity in item_counts.items())
        else:
            content.append("- Your backpack is empty.")
    elif section == "Equipments":
        content = ["Equipments:"]
        content.extend(f"{item_type.capitalize()}: {item if item else 'None'}" for item_type, item in main_character.equipments.items())
    elif section == "Abilities":
        content = ["Abilities:"]
        content.extend(f"- {ability}" for ability in main_character.abilities)
    elif section == "Quests":
        content = ["Active Quests:"]
        content.extend(f"- {quest}" for quest in main_character.quests)
        content.append("Completed Quests:")
        content.extend(f"- {quest}" for quest in main_character.concluded_quests)
    elif section == "Proficiencies":
        content = ["Proficiencies:"]
        content.extend(f"- {proficiency}" for proficiency in main_character.proficiencies)
    else:
        content = [f" {section}."]
    
    show_section(stdscr, section, content)

def show_section(stdscr: curses.window, title: str, content: list):
    """Display content of a section with navigation."""
    top_index = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        visible_height = height - 3  

        # Draw title
        draw_menu(stdscr, title, content, top_index, "Use ↑/↓ to navigate, 'q' to go back")

        stdscr.refresh()

        # Capture user input
        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            if top_index + visible_height < len(content):
                top_index += 1
        elif key == curses.KEY_UP:
            if top_index > 0:
                top_index -= 1
        elif key == ord('q'):
            break
