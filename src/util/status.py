import curses
from util.wrap_text import wrap_text
from characters.hero import Hero
from collections import Counter

def init_colors():
    """Initialize color pairs for curses."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected item (highlighted)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Normal text
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Title

def show_status(hero: Hero, stdscr: curses.window):
    """Display the hero's status with navigation."""
    init_colors()  # Initialize colors
    sections = [
        "Health: {}/{}".format(hero.health_points, hero.max_hp),
        "Gold: {}".format(hero.gold),
        "Experience: {}/{} (Level {})".format(hero.experience, hero.next_level_xp, hero.level),
        "Attack Points: {}".format(hero.attack_points),
        "Defense Points: {}".format(hero.defense_points),
        "Critical Hit Chance: {}%".format(hero.critical_hit_chance),
        "Dodge Chance: {}%".format(hero.dodge_chance),
        "Resistance Factor: {}".format(hero.resistance_factor),
        "Speed: {}".format(hero.speed),
        "Carry Weight: {}/{}".format(hero.weight, hero.carry_weight),
        "Equipments",
        "Backpack",
        "Abilities",
        "Quests",
        "Proficiencies",
        "Last Attack Damage: {}".format(hero.last_attack_damage),
        "Extra Actions: {}".format(hero.extra_actions),
    ]

    current_selection = 0
    top_index = 0

    while True:
        height, width = stdscr.getmaxyx()
        visible_height = height - 2  # Reserve space for instructions

        # Clear screen and draw title
        stdscr.clear()
        stdscr.addstr(0, 0, "=== Hero's Status ===".center(width), curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)

        # Draw sections
        for i in range(visible_height):
            idx = top_index + i
            if idx >= len(sections):
                break
            if idx == current_selection:
                stdscr.addstr(i + 1, 2, f"> {sections[idx]}", curses.color_pair(1))  # Highlight selection
            else:
                stdscr.addstr(i + 1, 2, sections[idx], curses.color_pair(2))  # Normal text

        # Navigation instructions
        stdscr.addstr(height - 1, 0, "Use ↑/↓ to navigate, ENTER to select, 'q' to quit.", curses.A_DIM)

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
            show_section_details(hero, stdscr, sections[current_selection])
        elif key == ord('q'):
            break

def show_section_details(hero: Hero, stdscr: curses.window, section: str):
    """Display details of a selected section."""
    if section == "Backpack":
        content = ["Backpack Contents:"]
        if hero.backpack:
            item_counts = Counter(hero.backpack)
            content.extend(f"- {quantity}x {item.name} (Value: {item.value}, Weight: {item.weight})"
                           for item, quantity in item_counts.items())
        else:
            content.append("- Your backpack is empty.")
    elif section == "Equipments":
        content = ["Equipments:"]
        content.extend(f"{item_type.capitalize()}: {item if item else 'None'}" for item_type, item in hero.equipments.items())
    elif section == "Abilities":
        content = ["Abilities:"]
        content.extend(f"- {ability}" for ability in hero.abilities)
    elif section == "Quests":
        content = ["Active Quests:"]
        content.extend(f"- {quest}" for quest in hero.quests)
        content.append("Completed Quests:")
        content.extend(f"- {quest}" for quest in hero.concluded_quests)
    elif section == "Proficiencies":
        content = ["Proficiencies:"]
        content.extend(f"- {proficiency}" for proficiency in hero.proficiencies)
    else:
        content = [f" {section}."]
    
    show_section(stdscr, section, content)

def show_section(stdscr: curses.window, title: str, content: list):
    """Display content of a section with navigation."""
    top_index = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        visible_height = height - 3  # Reserve space for title and instructions

        # Draw title
        stdscr.addstr(0, 0, title.center(width), curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)

        # Wrap content for proper display
        wrapped_content = []
        for line in content:
            wrapped_content.extend(wrap_text(line, width - 2))

        # Display content
        for i in range(visible_height):
            idx = top_index + i
            if idx >= len(wrapped_content):
                break
            stdscr.addstr(i + 2, 2, wrapped_content[idx], curses.color_pair(2))

        # Navigation instructions
        stdscr.addstr(height - 1, 0, "Use ↑/↓ to navigate, 'q' to go back.", curses.A_DIM)

        stdscr.refresh()

        # Capture user input
        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            if top_index + visible_height < len(wrapped_content):
                top_index += 1
        elif key == curses.KEY_UP:
            if top_index > 0:
                top_index -= 1
        elif key == ord('q'):
            break
