import os
import json
from datetime import datetime
from cryptography.fernet import Fernet
import curses
from characters.hero import Hero
from destinations.cave.owl_bear_cave import OwlBearCave
from destinations.forest.forest import Forest
from destinations.prismeer import City
from util.display_message import display_message
from global_state.global_state import get_game_state

SAVE_DIR = "saves"
KEY_FILE = "secret.key"

def load_or_generate_key():
    """Carrega ou gera uma chave de criptografia."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    return Fernet(key)

cipher = load_or_generate_key()

def save_game(stdscr: curses.window):
    """Permite ao jogador nomear o save e salva o estado do jogo em um arquivo criptografado."""
    os.makedirs(SAVE_DIR, exist_ok=True)

    input_active = True
    save_name = ""
    
    while input_active:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Título
        title = "=== Save Your Game ==="
        stdscr.attron(curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(1, (width - len(title)) // 2, title)
        stdscr.attroff(curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)

        # Instrução
        instructions = "Enter save name and press ENTER:"
        stdscr.attron(curses.A_DIM)
        stdscr.addstr(3, (width - len(instructions)) // 2, instructions)
        stdscr.attroff(curses.A_DIM)

        # Caixa de entrada centralizada
        input_y = height // 2
        input_x = (width - 30) // 2  # Limita a entrada a 30 caracteres
        stdscr.addstr(input_y, input_x - 2, "[", curses.color_pair(2))
        stdscr.addstr(input_y, input_x, save_name + ("_" if len(save_name) < 30 else ""), curses.color_pair(1))
        stdscr.addstr(input_y, input_x + len(save_name) + 1, "]", curses.color_pair(2))
        stdscr.refresh()

        key = stdscr.getch()

        if key == 10 and save_name:  # ENTER
            input_active = False
        elif key == 127 or key == curses.KEY_BACKSPACE:  # Backspace
            save_name = save_name[:-1]
        elif 32 <= key <= 126 and len(save_name) < 30:  # Caracteres imprimíveis
            save_name += chr(key)

    # Gera o nome final do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_file = os.path.join(SAVE_DIR, f"{save_name}_{timestamp}.dat")

    game_state = get_game_state()
    hero, prismeer, cave, forest, atual_location, combat_done = (
        game_state["hero"], game_state["prismeer"], game_state["cave"],
        game_state["forest"], game_state["atual_location"], game_state["combat_done"]
    )
    
    data = {
        "hero": hero.to_dict(),
        "prismeer": prismeer.to_dict(),
        "cave": cave.to_dict(),
        "forest": forest.to_dict(),
        "atual_location": atual_location,
        "combat_done": combat_done,
    }

    try:
        encrypted_data = cipher.encrypt(json.dumps(data).encode('utf-8'))

        with open(save_file, 'wb') as file:
            file.write(encrypted_data)

        selected_index = 0
        options = ["Continue"]

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # Título de sucesso
            title = "=== Game Saved Successfully ==="
            stdscr.attron(curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)
            stdscr.addstr(1, (width - len(title)) // 2, title)
            stdscr.attroff(curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)

            # Mensagem de confirmação
            message = f"Save '{save_name}' created!"
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(3, (width - len(message)) // 2, message)
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            # Instruções
            instructions = "Press ENTER to continue"
            stdscr.attron(curses.A_DIM)
            stdscr.addstr(height - 3, (width - len(instructions)) // 2, instructions)
            stdscr.attroff(curses.A_DIM)

            # Centraliza a opção "Continue"
            start_y = height // 2
            for idx, option in enumerate(options):
                y = start_y + idx
                option_text = f"> {option}" if idx == selected_index else f"  {option}"
                x = (width - len(option_text)) // 2

                if idx == selected_index:
                    stdscr.attron(curses.color_pair(1) | curses.A_REVERSE)
                    stdscr.addstr(y, x, option_text)
                    stdscr.attroff(curses.color_pair(1) | curses.A_REVERSE)
                else:
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(y, x, option_text)
                    stdscr.attroff(curses.color_pair(2))

            stdscr.refresh()

            key = stdscr.getch()
            if key == 10:  # ENTER
                return

    except Exception as e:
        display_message(stdscr, f"Error saving the game: {e}", curses.color_pair(2))

def load_game(stdscr: curses.window, save_file: str):
    """Carrega um jogo salvo a partir de um arquivo criptografado."""
    try:
        with open(save_file, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)
        data = json.loads(decrypted_data.decode('utf-8'))

        # Exibe mensagem de sucesso
        stdscr.clear()
        stdscr.addstr(0, 0, "=== Game Loaded ===", curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(2, 0, "Game loaded successfully!", curses.color_pair(1))
        stdscr.refresh()
        curses.napms(2000)  # Pausa para exibir a mensagem

        return data
    except FileNotFoundError:
        display_message(stdscr, f"File {save_file} not found.", curses.color_pair(2))
    except Exception as e:
        display_message(stdscr, f"Error loading the game: {e}", 40000, curses.color_pair(2))

    return None

def list_saves(stdscr: curses.window):
    """Exibe a lista de saves disponíveis com navegação e seleção, ordenada por data de criação."""
    if not os.path.exists(SAVE_DIR):
        display_message(stdscr, "No saves found.", curses.color_pair(2))
        return []

    # Obtém a lista de saves, ordenada por data de criação (mais recente primeiro)
    saves = sorted(
        [f for f in os.listdir(SAVE_DIR) if f.endswith('.dat')],
        key=lambda x: os.path.getctime(os.path.join(SAVE_DIR, x)),
        reverse=True
    )

    if not saves:
        display_message(stdscr, "No saves available.", curses.color_pair(2))
        return []

    # Configuração de cores (Certifique-se de inicializar o curses antes de chamar esta função)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Seleção destacada
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Texto normal

    selected_index = 0  # Índice da opção selecionada
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Título centralizado
        title = "=== Select a Save ==="
        stdscr.addstr(1, (width - len(title)) // 2, title, curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)

        # Instruções centralizadas
        instructions = "Use ↑/↓ to navigate, ENTER to select, 'q' to quit."
        stdscr.addstr(3, (width - len(instructions)) // 2, instructions, curses.A_DIM)

        # Calcula a posição vertical para centralizar a lista de saves
        start_y = (height - len(saves)) // 2
        if start_y < 4:  # Garante que a lista não sobreponha o título e as instruções
            start_y = 4

        # Desenha a lista de saves centralizada
        for idx, save in enumerate(saves):
            y = start_y + idx
            if y >= height - 1:  # Evita escrever fora da tela
                break
            save_text = f"> {save}" if idx == selected_index else f"  {save}"
            x = (width - len(save_text)) // 2  # Centraliza horizontalmente
            if idx == selected_index:
                stdscr.addstr(y, x, save_text, curses.color_pair(1))  # Usa a cor do texto destacado
            else:
                stdscr.addstr(y, x, save_text, curses.color_pair(2))  # Usa a cor do texto normal

        stdscr.refresh()

        # Captura a tecla pressionada
        key = stdscr.getch()

        if key == ord('q'):  # Tecla 'q' para sair
            break
        elif key == curses.KEY_UP:  # Seta para cima
            selected_index = (selected_index - 1) % len(saves)
        elif key == curses.KEY_DOWN:  # Seta para baixo
            selected_index = (selected_index + 1) % len(saves)
        elif key == 10:  # Tecla ENTER
            save_file = os.path.join(SAVE_DIR, saves[selected_index])
            return load_game(stdscr, save_file)


def load_game(stdscr: curses.window, save_file: str):
    try:
        with open(save_file, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)
        data = json.loads(decrypted_data.decode('utf-8'))

        selected_index = 0
        options = ["Continue"]

        hero = Hero.from_dict(data["hero"])
        prismeer = City.from_dict(data["prismeer"])
        cave = OwlBearCave.from_dict(data["cave"])
        forest = Forest.from_dict(data["forest"])
        atual_location = data["atual_location"]

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # Título centralizado
            title = "=== Game Loaded Successfully ==="
            stdscr.attron(curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)
            stdscr.addstr(1, (width - len(title)) // 2, title)
            stdscr.attroff(curses.color_pair(3) | curses.A_BOLD | curses.A_UNDERLINE)

            message = "Your adventure awaits!"
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(3, (width - len(message)) // 2, message)
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            instructions = "Press ENTER to continue"
            stdscr.attron(curses.A_DIM)
            stdscr.addstr(height - 3, (width - len(instructions)) // 2, instructions)
            stdscr.attroff(curses.A_DIM)

            start_y = height // 2
            for idx, option in enumerate(options):
                y = start_y + idx
                option_text = f"> {option}" if idx == selected_index else f"  {option}"
                x = (width - len(option_text)) // 2

                if idx == selected_index:
                    stdscr.attron(curses.color_pair(1) | curses.A_REVERSE)
                    stdscr.addstr(y, x, option_text)
                    stdscr.attroff(curses.color_pair(1) | curses.A_REVERSE)
                else:
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(y, x, option_text)
                    stdscr.attroff(curses.color_pair(2))

            stdscr.refresh()

            key = stdscr.getch()
            if key == 10: 
                return hero, cave, prismeer, forest, atual_location

    except Exception as e:
        display_message(stdscr, f"Error loading save: {e}", curses.color_pair(2))

    return None

def load_game_and_update(stdscr: curses.window):
    """Carrega um jogo salvo e atualiza o estado global."""
    result = list_saves(stdscr)

    if result:
        hero, cave, prismeer, forest, atual_location = result
        return {
            "is_new_game": False,
            "hero": hero,
            "cave": cave,
            "prismeer": prismeer,
            "forest": forest,
            "atual_location": atual_location
        }
    return None