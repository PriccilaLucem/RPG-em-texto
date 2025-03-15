from characters.hero import Hero
from destinations.cave.owl_bear_cave import OwlBearCave
from destinations.forest.forest import Forest 
from destinations.prismeer import City
from util.display_message import display_message
import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
import curses
from global_state.global_state import get_game_state
SAVE_DIR = "saves"
KEY_FILE = "secret.key"

def load_or_generate_key():
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
    os.makedirs(SAVE_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_file = os.path.join(SAVE_DIR, f"save_{timestamp}.dat")
    game_state = get_game_state()
    hero, prismeer, cave, forest, atual_location, combat_done =  game_state["hero"], game_state["prismeer"], game_state["cave"], game_state["forest"], game_state["atual_location"], game_state["combat_done"]
    
    data = {
        "hero": hero.to_dict(),
        "prismeer": prismeer.to_dict(),
        "cave": cave.to_dict() ,
        "forest": forest.to_dict(),
        "atual_location": atual_location,
        "combat_done": combat_done,
    }

    try:
        encrypted_data = cipher.encrypt(json.dumps(data).encode('utf-8'))

        with open(save_file, 'wb') as file:
            file.write(encrypted_data)

        stdscr.addstr(f"Game saved and encrypted in {save_file}\n")
        stdscr.refresh()
    except Exception as e:
        display_message(stdscr, f"Error saving the game: {e}")

    display_message(stdscr, "Game saved!")

def load_game(stdscr, save_file: str):
    try:
        with open(save_file, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)
        data = json.loads(decrypted_data.decode('utf-8'))
        display_message(stdscr, "Game loaded successfully!")
        return data
    except FileNotFoundError:
        display_message(stdscr, f"File {save_file} not found.")
    except Exception as e:
        display_message(stdscr, f"Error loading the game: {e}")

    return None

def list_saves(stdscr: curses.window):
    if not os.path.exists(SAVE_DIR):
        display_message(stdscr, "No saves found.")
        return []

    saves = [f for f in os.listdir(SAVE_DIR) if f.endswith('.dat')]
    if not saves:
        display_message(stdscr, "No saves available.")
        return []

    stdscr.clear()
    stdscr.addstr("Select a save:\n")

    for idx, save in enumerate(saves, 1):
        stdscr.addstr(f"{idx}. {save}\n")

    stdscr.refresh()

    try:
        key = stdscr.getch() - ord('0')
        if 1 <= key <= len(saves):
            selected_save = saves[key - 1]
            save_file = os.path.join(SAVE_DIR, selected_save)
            data = load_game(stdscr, save_file)
            hero = Hero.from_dict(data["hero"])
            prismeer = City.from_dict(data["prismeer"])
            cave = OwlBearCave.from_dict(data["cave"])
            forest = Forest.from_dict(data["forest"])

            return hero, cave, prismeer, forest, data["atual_location"]
    except Exception as e:
        display_message(stdscr, f"Erro ao carregar dados do save, {e}")
    return None

def load_game_and_update(stdscr: curses.window):
    
    result = list_saves(stdscr)
    
    if result:
        hero, cave, prismeer, forest, atual_location = result
        return {
            "is_new_game": False,
            "hero":hero,
            "owl_bear_cave":cave, 
            "prismeer": prismeer, 
            "regular_forest":forest,
            "atual_location": atual_location
            }
    return None
