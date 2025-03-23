import os
import json
from datetime import datetime
from cryptography.fernet import Fernet
import curses
from characters.main_character import MainCharacter
from destinations.cave.owl_bear_cave import OwlBearCave
from destinations.prismeer import City
from util.display_message import display_message, draw_menu
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
        instructions = "Enter save name and press ENTER:"
        options = [save_name + ("_" if len(save_name) < 30 else "")]  # Simulate input box as an option

        # Draw the menu with the input box
        draw_menu(stdscr, title, options, 0)

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


 # Converte o item para dicionário, se possível

    
    # Atribui o item correspondente ou o dicionário convertido
    data= {}
    for key, value in get_game_state().items():
        if hasattr(value, "to_dict"):
            data[key] = value.to_dict()
        else:
            data[key] = value
    try:
        encrypted_data = cipher.encrypt(json.dumps(data).encode('utf-8'))

        with open(save_file, 'wb') as file:
            file.write(encrypted_data)

        # Exibe mensagem de sucesso
        title = "=== Game Saved Successfully ==="
        message = f"Save '{save_name}' created!"
        options = ["Continue"]

        # Draw the success menu
        selected_index = 0
        while True:
            draw_menu(stdscr, title, options, selected_index)
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif key == 10:  # ENTER
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

    selected_index = 0  # Índice da opção selecionada
    while True:
        title = "=== Select a Save ==="
        # Draw the menu with the list of saves
        
        draw_menu(stdscr, title, saves, selected_index)

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
        # Load and decrypt the save file
        with open(save_file, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        data = json.loads(decrypted_data.decode('utf-8'))

        # Deserialize game data
        main_character = MainCharacter.from_dict(data["MainCharacter"])
        prismeer = City.from_dict(data["prismeer"])
        cave = OwlBearCave.from_dict(data["cave"])
        atual_location = data["atual_location"]

        # Display success message and wait for user input
        selected_index = 0
        options = ["Continue"]

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # Título centralizado
            title = "=== Game Loaded Successfully ==="
            title_x = (width - len(title)) // 2
            stdscr.addstr(2, title_x, title, curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE)

            # Mensagem centralizada
            message = "Your adventure awaits!"
            message_x = (width - len(message)) // 2
            stdscr.addstr(4, message_x, message, curses.color_pair(11) | curses.A_BOLD)

            # Instruções centralizadas
            instructions = "Press ENTER to continue"
            instructions_x = (width - len(instructions)) // 2
            stdscr.addstr(height - 3, instructions_x, instructions, curses.color_pair(1) | curses.A_DIM)

            # Opções do menu (apenas "Continue" neste caso)
            start_y = (height - len(options)) // 2
            for i, option in enumerate(options):
                option_x = (width - len(option)) // 2
                if i == selected_index:
                    stdscr.addstr(start_y + i, option_x, option, curses.color_pair(1) | curses.A_UNDERLINE)
            stdscr.refresh()

            # Captura a tecla pressionada
            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif key == 10:  # ENTER
                # Return the loaded game data
                return main_character, cave, prismeer, atual_location

    except FileNotFoundError:
        display_message(stdscr, f"File {save_file} not found.", curses.color_pair(2))
    except Exception as e:
        display_message(stdscr, f"Error loading the game: {e}", curses.color_pair(2))

    return None


def load_game_and_update(stdscr: curses.window):
    result = list_saves(stdscr)

    if result:
        MainCharacter, cave, prismeer, forest, atual_location = result
        return {
            "is_new_game": False,
            "MainCharacter": MainCharacter,
            "cave": cave,
            "prismeer": prismeer,
            "forest": forest,
            "atual_location": atual_location
        }
    return None