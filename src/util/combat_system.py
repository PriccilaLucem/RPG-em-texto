from typing import Union, List, TYPE_CHECKING
if TYPE_CHECKING:
    from characters.main_character import MainCharacter
    from models.enemy_model import EnemyModel
import random
import curses
from enums.skill_type_enum import SkillTypeEnum
from util.display_message import display_message, draw_menu, display_message_log, draw_menu_with_history


def roll_dice(stdscr: curses.window, message: str) -> int:
    """Simulates a dice roll with animation."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Exibe a mensagem centralizada
    display_message(stdscr, message, 500, curses.color_pair(1))

    # Simula a animação do dado
    for _ in range(10):
        roll = random.randint(1, 20)
        display_message(stdscr, f"Rolling... {roll}", 100, curses.color_pair(2))

    final_roll = random.randint(1, 20)
    display_message(stdscr, f"Final Roll: {final_roll}", 1000, curses.color_pair(1))
    return final_roll


def attack(attacker: Union["EnemyModel", "MainCharacter"], defenser: Union["EnemyModel", "MainCharacter"], stdscr: curses.window) -> int:
    """Calculates the damage of an attack."""
    roll = roll_dice(stdscr, f"{attacker.name} is rolling for attack!")
    base_damage = (attacker.attack_points + roll * 0.5) * attacker.attack_multiplier - defenser.defense_points
    if base_damage < 0:
        base_damage = (defenser.defense_points - attacker.attack_points)

    base_damage *= defenser.resistance_factor
    crit_roll = roll_dice(stdscr, f"{attacker.name} is rolling for critical hit!")
    if crit_roll < attacker.critical_hit_chance:
        critical_damage = base_damage * 1.5
        return int(critical_damage)

    return int(base_damage)


def defend(defender: Union["EnemyModel", "MainCharacter"], attacker: Union["EnemyModel", "MainCharacter"], stdscr: curses.window) -> int:
    """Calculates the mitigated damage when defending."""
    roll = roll_dice(stdscr, f"{defender.name} is rolling for defense!")
    base_damage = (attacker.attack_points + roll) - defender.defense_points

    if base_damage < 0:
        base_damage = 0

    mitigated_damage = base_damage * defender.resistance_factor

    crit_roll = roll_dice(stdscr, f"{defender.name} is rolling for critical defense!")
    if random.random() < defender.critical_hit_chance * crit_roll/20:
        mitigated_damage *= 0.5

    return int(mitigated_damage)


def use_skill(
    caster: Union["MainCharacter", "EnemyModel"],
    stdscr: curses.window,
    target: Union["MainCharacter", "EnemyModel"],
    message_log: List[str]
) -> str:
    """Allows the player or enemy to use a skill."""
    if isinstance(caster, MainCharacter):
        # Exibe o menu de seleção de habilidades
        skill_options = [f"{ability.name} (Cooldown: {ability.current_cooldown})" for ability in caster.abilities]
        selected_index = 0
        while True:
            draw_menu(stdscr, "=== Choose a Skill ===", skill_options, selected_index)
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = max(0, selected_index - 1)
            elif key == curses.KEY_DOWN:
                selected_index = min(len(skill_options) - 1, selected_index + 1)
            elif key == ord('\n'):  # ENTER key
                skill = caster.abilities[selected_index]
                break
    else:
        skill = random.choice(caster.abilities)

    if not skill.is_ready():
        message = f"Skill {skill.name} is on cooldown for {skill.current_cooldown} turns!"
        message_log.append(message)
        return message

    if skill.type == SkillTypeEnum.DAMAGE:
        damage = skill.damage
        target.health_points = max(0, target.health_points - damage)
        message = f"{caster.name} used {skill.name} and dealt {damage} damage to {target.name}!"
    elif skill.type == SkillTypeEnum.HEAL:
        heal_amount = skill.effect_value
        caster.health_points = min(caster.max_hp, caster.health_points + heal_amount)
        message = f"{caster.name} used {skill.name} and healed {heal_amount} HP!"
    elif skill.type == SkillTypeEnum.BUFF:
        buff_amount = skill.effect_value
        caster.attack_points += buff_amount
        message = f"{caster.name} used {skill.name} and increased attack by {buff_amount}!"
    elif skill.type == SkillTypeEnum.DEBUFF:
        debuff_amount = skill.effect_value
        target.defense_points = max(0, target.defense_points - debuff_amount)
        message = f"{caster.name} used {skill.name} and reduced {target.name}'s defense by {debuff_amount}!"
    elif skill.type == SkillTypeEnum.UTILITY:
        message = f"{caster.name} used {skill.name} and activated a special effect!"
    else:
        message = f"{caster.name} tried to use {skill.name}, but it had no effect."

    skill.current_cooldown = skill.cooldown
    message_log.append(message)
    return f"Skill {skill.name} used successfully!"


def combat(stdscr: curses.window, main_character: "MainCharacter", enemy: "EnemyModel") -> bool:
    """Executes combat between the main_character and the enemy."""
    def roll_initiative(character: Union["MainCharacter", "EnemyModel"]) -> int:
        """Rolls initiative for a character."""
        roll = roll_dice(stdscr, f"{character.name} is rolling for initiative!")
        total = roll + character.speed
        message = f"{character.name} rolls a {total} (Roll: {roll} + Speed: {character.speed})"
        message_log.append(message)
        return total

    def perform_action(character: Union["MainCharacter", "EnemyModel"], opponent: Union["MainCharacter", "EnemyModel"]) -> None:
        """Chooses and performs an action for the character."""
        action: str = random.choices(
            ["attack", "use_skill", "defend"],
            weights=[4, 2, 1],
            k=1
        )[0]

        if action == "attack":
            damage: int = attack(character, opponent, stdscr)
            opponent.health_points -= damage
            message = f"{character.name} attacks {opponent.name} and deals {damage} damage!"
            message_log.append(message)
        elif action == "use_skill" and character.abilities:
            message: str = use_skill(character, stdscr, opponent, message_log)
            message_log.append(message)
        elif action == "defend":
            mitigated_damage: int = defend(character, opponent, stdscr)
            message = f"{character.name} braces for the next attack and mitigates {mitigated_damage} damage!"
            message_log.append(message)

    def main_character_action_input() -> str:
        """Gets the main_character's action from the player using arrow navigation."""
        options = ["Attack", "Defend", "Use Skill"]
        if not main_character.abilities:  # Remove "Use Skill" if main_character has no abilities
            options.pop()
        selected_index = 0  # Index of the selected option

        while True:
            draw_menu_with_history(stdscr, "=== Choose an Action ===", "\n".join(message_log[-5:]), options, selected_index)
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = max(0, selected_index - 1)  # Move up
            elif key == curses.KEY_DOWN:
                selected_index = min(len(options) - 1, selected_index + 1)  # Move down
            elif key == ord('\n'):  # ENTER key
                return options[selected_index]  # Return corresponding action

    def reduce_all_cooldowns(character: Union["MainCharacter", "EnemyModel"]) -> None:
        """Reduces the cooldown of all abilities."""
        for ability in character.abilities:
            ability.reduce_cooldown()

    # Initialize message log
    message_log: List[str] = []
    message_log.append(f"⚔️ Combat begins between {main_character.name} and {enemy.name}!")
    message_log.append(f"{main_character.name}: {main_character.health_points} HP, {enemy.name}: {enemy.health_points} HP")
    display_message_log(stdscr, message_log)
    curses.napms(2000)  # Pause to allow the player to read the log

    turn: int = 0

    while main_character.health_points > 0 and enemy.health_points > 0:
        turn += 1
        message_log.append(f"--- Turn {turn} ---")
        display_message(stdscr, f"--- Turn {turn} ---", 1000)

        # Roll initiative and determine turn order
        main_character_roll = roll_initiative(main_character)
        enemy_roll = roll_initiative(enemy)
        first_attacker, second_attacker = (main_character, enemy) if main_character_roll >= enemy_roll else (enemy, main_character)

        # Perform actions for each attacker
        for attacker, defender in [(first_attacker, second_attacker), (second_attacker, first_attacker)]:
            if attacker.health_points <= 0 or defender.health_points <= 0:
                break

            if attacker == main_character:
                main_character_action = main_character_action_input()
                if main_character_action == "Attack":
                    damage = attack(main_character, enemy, stdscr)
                    enemy.health_points -= damage
                    message_log.append(f"{main_character.name} attacks {enemy.name} and deals {damage} damage!")
                elif main_character_action == "Use Skill":
                    message = use_skill(main_character, stdscr, enemy, message_log)
                    message_log.append(message)
                elif main_character_action == "Defend":
                    mitigated_damage = defend(main_character, enemy, stdscr)
                    message_log.append(f"{main_character.name} braces for the next attack and mitigates {mitigated_damage} damage!")
            else:
                perform_action(attacker, defender)

            if defender.health_points <= 0:
                message_log.append(f"💥 {defender.name} is defeated!")
                break

        reduce_all_cooldowns(main_character)
        reduce_all_cooldowns(enemy)

        # Display updated HP and message log
        message_log.append(f"{main_character.name}: {main_character.health_points} HP, {enemy.name}: {enemy.health_points} HP")
        display_message_log(stdscr, message_log)
        curses.napms(2000)  # Pause to allow the player to read the log

    if main_character.health_points > 0:
        display_message(stdscr, f"🏆 {main_character.name} is victorious!", 2000, curses.color_pair(1))
        enemy.drop_items(main_character)
    else:
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        display_message(stdscr, f"💀 {main_character.name} has been defeated!", 2000, curses.color_pair(1))

    return main_character.health_points > 0  
