from characters.hero import Hero
from models.enemy_model import EnemyModel
from typing import Union, List
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


def attack(attacker: Union[EnemyModel, Hero], defenser: Union[EnemyModel, Hero], stdscr: curses.window) -> int:
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


def defend(defender: Union[EnemyModel, Hero], attacker: Union[EnemyModel, Hero], stdscr: curses.window) -> int:
    """Calculates the mitigated damage when defending."""
    roll = roll_dice(stdscr, f"{defender.name} is rolling for defense!")
    base_damage = (attacker.attack_points + roll) - defender.defense_points

    if base_damage < 0:
        base_damage = 0

    mitigated_damage = base_damage * defender.resistance_factor

    crit_roll = roll_dice(stdscr, f"{defender.name} is rolling for critical defense!")
    if random.random() < defender.critical_hit_chance:
        mitigated_damage *= 0.5

    return int(mitigated_damage)


def use_skill(
    caster: Union[Hero, EnemyModel],
    stdscr: curses.window,
    target: Union[Hero, EnemyModel],
    message_log: List[str]
) -> str:
    """Allows the player or enemy to use a skill."""
    if isinstance(caster, Hero):
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


def combat(stdscr: curses.window, hero: Hero, enemy: EnemyModel) -> bool:
    """Executes combat between the hero and the enemy."""
    def roll_initiative(character: Union[Hero, EnemyModel]) -> int:
        """Rolls initiative for a character."""
        roll = roll_dice(stdscr, f"{character.name} is rolling for initiative!")
        total = roll + character.speed
        message = f"{character.name} rolls a {total} (Roll: {roll} + Speed: {character.speed})"
        message_log.append(message)
        return total

    def perform_action(character: Union[Hero, EnemyModel], opponent: Union[Hero, EnemyModel]) -> None:
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

    def hero_action_input() -> str:
        """Gets the hero's action from the player using arrow navigation."""
        options = ["Attack", "Defend", "Use Skill"]
        if not hero.abilities:  # Remove "Use Skill" if hero has no abilities
            options.remove("Use Skill")
        selected_index = 0  # Index of the selected option

        while True:
            draw_menu_with_history(stdscr, "=== Choose an Action ===", "\n".join(message_log[-5:]), options, selected_index)
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = max(0, selected_index - 1)  # Move up
            elif key == curses.KEY_DOWN:
                selected_index = min(len(options) - 1, selected_index + 1)  # Move down
            elif key == ord('\n'):  # ENTER key
                return ["A", "S", "D"][selected_index]  # Return corresponding action

    def reduce_all_cooldowns(character: Union[Hero, EnemyModel]) -> None:
        """Reduces the cooldown of all abilities."""
        for ability in character.abilities:
            ability.reduce_cooldown()

    # Initialize message log
    message_log: List[str] = []
    message_log.append(f"⚔️ Combat begins between {hero.name} and {enemy.name}!")
    message_log.append(f"{hero.name}: {hero.health_points} HP, {enemy.name}: {enemy.health_points} HP")
    display_message_log(stdscr, message_log)
    curses.napms(2000)  # Pause to allow the player to read the log

    turn: int = 0

    while hero.health_points > 0 and enemy.health_points > 0:
        turn += 1
        message_log.append(f"--- Turn {turn} ---")
        display_message(stdscr, f"--- Turn {turn} ---", 1000)

        # Roll initiative and determine turn order
        hero_roll = roll_initiative(hero)
        enemy_roll = roll_initiative(enemy)
        first_attacker, second_attacker = (hero, enemy) if hero_roll >= enemy_roll else (enemy, hero)

        # Perform actions for each attacker
        for attacker, defender in [(first_attacker, second_attacker), (second_attacker, first_attacker)]:
            if attacker.health_points <= 0 or defender.health_points <= 0:
                break

            if attacker == hero:
                hero_action = hero_action_input()
                if hero_action == "A":
                    damage = attack(hero, enemy, stdscr)
                    enemy.health_points -= damage
                    message_log.append(f"{hero.name} attacks {enemy.name} and deals {damage} damage!")
                elif hero_action == "S":
                    message = use_skill(hero, stdscr, enemy, message_log)
                    message_log.append(message)
                elif hero_action == "D":
                    mitigated_damage = defend(hero, enemy, stdscr)
                    message_log.append(f"{hero.name} braces for the next attack and mitigates {mitigated_damage} damage!")
            else:
                perform_action(attacker, defender)

            if defender.health_points <= 0:
                message_log.append(f"💥 {defender.name} is defeated!")
                break

        reduce_all_cooldowns(hero)
        reduce_all_cooldowns(enemy)

        # Display updated HP and message log
        message_log.append(f"{hero.name}: {hero.health_points} HP, {enemy.name}: {enemy.health_points} HP")
        display_message_log(stdscr, message_log)
        curses.napms(2000)  # Pause to allow the player to read the log

    if hero.health_points > 0:
        message_log.append(f"🏆 {hero.name} is victorious!")
        enemy.drop_items(hero)
    else:
        message_log.append(f"💔 {hero.name} has been defeated by {enemy.name}.")

    display_message_log(stdscr, message_log)
    curses.napms(3000)  # Pause before exiting combat

    return hero.health_points > 0