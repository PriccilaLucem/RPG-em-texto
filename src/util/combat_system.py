from characters.hero import Hero
from models.enemy_model import EnemyModel
from typing import Union, Callable
import random
from util.display_message import display_message
import curses
from enums.skill_type_enum import SkillTypeEnum

def attack(attacker: Union[EnemyModel, Hero], defenser : Union[EnemyModel, Hero]) -> int:

    roll = random.randint(1,20)
    base_damage = (attacker.attack_points + roll * 0.5) * attacker.attack_multiplier  - defenser.defense_points
    if base_damage < 0:
        base_damage = (defenser.defense_points - attacker.attack_points)

    base_damage *= defenser.resistance_factor
    roll = random.randint(1,20)
    if roll < attacker.critical_hit_chance:
        critical_damage = base_damage * 1.5
        return int(critical_damage)

    return int(base_damage)

def defend(defender: Union[EnemyModel, Hero], attacker: Union[EnemyModel, Hero]) -> int:
    
    roll = random.randint(1, 20)
    
    base_damage = (attacker.attack_points + roll)  - defender.defense_points

    if base_damage < 0:
        base_damage = 0

    mitigated_damage = base_damage * defender.resistance_factor

    if random.random() < defender.critical_hit_chance:
        mitigated_damage *= 0.5  

    return int(mitigated_damage)


def use_skill(
    caster: Union[Hero, EnemyModel],
    stdscr: curses.window,
    target: Union[Hero, EnemyModel]
) -> str:
    if isinstance(caster, Hero):
        stdscr.addstr("Escolha a habilidade pelo ID (número): ")
        stdscr.refresh()

        while True:
            skill_id = stdscr.getch()
            try:
                skill_id = int(chr(skill_id))
            except ValueError:
                stdscr.addstr("ID da habilidade inválido. Tente novamente.\n")
                stdscr.refresh()
                continue
            
            skill = next((ability for ability in caster.abilities if ability.id == skill_id), None)
            if skill is None:
                stdscr.addstr(f"Habilidade com ID {skill_id} não encontrada. Tente novamente.\n")
                stdscr.refresh()
                continue
            break
    else:
        skill = random.choice(caster.abilities)

    if not skill.is_ready():
        return f"A habilidade {skill.name} está em cooldown por {skill.current_cooldown} turnos!"

    if skill.type == SkillTypeEnum.DAMAGE:
        damage = skill.damage
        target.health_points = max(0, target.health_points - damage)
        stdscr.addstr(f"{caster.name} usou {skill.name} causando {damage} de dano em {target.name}!\n")

    elif skill.type == SkillTypeEnum.HEAL:
        heal_amount = skill.effect_value
        caster.health_points = min(caster.max_hp, caster.health_points + heal_amount)
        stdscr.addstr(f"{caster.name} usou {skill.name} curando {heal_amount} pontos de vida!\n")

    elif skill.type == SkillTypeEnum.BUFF:
        buff_amount = skill.effect_value
        caster.attack_points += buff_amount
        stdscr.addstr(f"{caster.name} usou {skill.name} aumentando seu ataque em {buff_amount}!\n")

    elif skill.type == SkillTypeEnum.DEBUFF:
        debuff_amount = skill.effect_value
        target.defense_points = max(0, target.defense_points - debuff_amount)
        stdscr.addstr(f"{caster.name} usou {skill.name} reduzindo a defesa de {target.name} em {debuff_amount}!\n")

    elif skill.type == SkillTypeEnum.UTILITY:
        stdscr.addstr(f"{caster.name} usou {skill.name}, ativando um efeito especial!\n")

    else:
        stdscr.addstr(f"{caster.name} tentou usar {skill.name}, mas não teve efeito.\n")

    skill.current_cooldown = skill.cooldown
    stdscr.refresh()

    return f"Habilidade {skill.name} utilizada com sucesso!"



def combat(stdscr: curses.window, hero: Hero, enemy: EnemyModel) -> bool:
    def roll_initiative(character: Hero | EnemyModel) -> int:
        roll = random.randint(1, 20) + character.speed
        display_message(
            stdscr,
            f"{character.name} rolls a {roll} (Roll: {roll - character.speed} + Speed: {character.speed})",
            1500
        )
        return roll

    def perform_action(character: Union[Hero, EnemyModel], opponent: Union[Hero, EnemyModel]) -> None:
        """Escolhe e realiza uma ação para o personagem."""
        action: str = random.choices(
            ["attack", "use_skill", "defend"], 
            weights=[4, 2, 1],  
            k=1  
        )[0]

        if action == "attack":
            damage: int = attack(character, opponent)
            opponent.health_points -= damage
            display_message(
                stdscr,
                f"{character.name} attacks {opponent.name} and deals {damage} damage!"
            )

        elif action == "use_skill" and character.abilities:
            message: str = use_skill(character, stdscr, opponent)
            display_message(stdscr, message, 1000)

        elif action == "defend":
            mitigated_damage: int = defend(character, opponent)
            display_message(
                stdscr,
                f"{character.name} braces for the next attack and mitigates {mitigated_damage} damage!",
                1000
            )

    def hero_action_input() -> str:
        """Obtém a ação do herói do jogador."""
        stdscr.addstr(0, 0, "Press A to Attack, S to use Skill, or D to Defend: ")
        stdscr.refresh()
        while True:
            hero_action: str = chr(stdscr.getch()).upper()
            if hero_action in actions:
                return hero_action
            display_message(stdscr, "Invalid action! Try again.", 1000)

    def reduce_all_cooldowns(character: Union[Hero, EnemyModel]) -> None:
        """Reduz os tempos de recarga de todas as habilidades."""
        for ability in character.abilities:
            ability.reduce_cooldown()

    actions: dict[str, Callable[[], None]] = {
        "A": lambda: attack(hero, enemy),
        "D": lambda: display_message(stdscr, "Hero defends!"),
        "S": lambda: use_skill(hero, stdscr, enemy) if hero.abilities else display_message(stdscr, "Hero does not have any abilities!", 1000)
    }

    display_message(stdscr, f"⚔️ Combat begins between Hero and {enemy.name}!", 1000)
    display_message(stdscr, f"Hero: {hero.health_points} HP, {enemy.name}: {enemy.health_points} HP\n", 2000)

    turn: int = 0

    while hero.health_points > 0 and enemy.health_points > 0:
        turn += 1
        display_message(stdscr, f"--- Turn {turn} ---", 1000)

        hero_roll: int = roll_initiative(hero)
        enemy_roll: int = roll_initiative(enemy)

        first_attacker, second_attacker = (hero, enemy) if hero_roll >= enemy_roll else (enemy, hero)

        for attacker, defender in [(first_attacker, second_attacker), (second_attacker, first_attacker)]:
            if attacker.health_points <= 0 or defender.health_points <= 0:
                break

            if attacker == hero:
                hero_action: str = hero_action_input()
                if hero_action == "A":
                    damage = attack(hero, enemy)
                    enemy.health_points -= damage
                    display_message(stdscr, f"{hero.name} attacks {enemy.name} and deals {damage} damage!")
                elif hero_action == "S":
                    message = use_skill(hero, stdscr, enemy)
                    display_message(stdscr, message, 1000)
                elif hero_action == "D":
                    mitigated_damage = defend(hero, enemy)
                    display_message(stdscr, f"{hero.name} braces for the next attack and mitigates {mitigated_damage} damage!", 1000)
            else:
                perform_action(attacker, defender)

            if defender.health_points <= 0:
                display_message(stdscr, f"💥 {defender.name} is defeated!", 1000)
                break

        reduce_all_cooldowns(hero)
        reduce_all_cooldowns(enemy)

        display_message(stdscr, f"\nHero: {hero.health_points} HP, {enemy.name}: {enemy.health_points} HP\n", 2000)

    if hero.health_points > 0:
        display_message(stdscr, "🏆 Hero is victorious!", 2000)
        return True
    else:
        display_message(stdscr, f"💔 Hero has been defeated by {enemy.name}.", 2000)
        return False
