from threading import Thread, Event
from pynput import keyboard
import queue
import time
from destinations.prismeer.city import City
from characters.hero import Hero
from destinations.prismeer import city_menu
from history.history import init_of_the_history
from commands_allowed import game_init

command_queue = queue.Queue()
comando = []
main_character = Hero()
prismeer = City()
exit_event = Event()  

def tecla_pressionada(key):
    """Handle keypress events."""
    global comando

    try:
        if key == keyboard.Key.enter:
            input_usuario = ''.join(comando).strip().upper()
            comando.clear()  

            if input_usuario == "P":
                print("You arrived at Prismeer!\n")
                city_menu(prismeer, main_character)  
            elif input_usuario == "EXIT":
                print("Global command received: Exiting...")
                command_queue.put("EXIT")
                exit_event.set()  
            elif input_usuario == "B":
                print("Displaying inventory...\n")
                main_character.show_backpack() 
            else:
                game_init()
                
        elif hasattr(key, 'char') and key.char is not None:
            comando.append(key.char)

        elif key == keyboard.Key.backspace:
            if comando:
                comando.pop()
    except Exception as e:  
        print(f"Error processing key press: {e}")


def start_listening():
    def stop_listener(listener):
        exit_event.wait()
        listener.stop()  

    with keyboard.Listener(on_press=tecla_pressionada) as listener:
        stop_thread = Thread(target=stop_listener, args=(listener,), daemon=True)
        stop_thread.start()
        listener.join()


def process_global_commands():
    """Process commands from the global command queue."""
    while True:
        if not command_queue.empty():
            command = command_queue.get()
            if command == "EXIT":
                print("Exiting the game...")
                break


def main_game_loop():

    init_of_the_history()
    print(game_init())
    while not exit_event.is_set():
        time.sleep(0.1)
        if not command_queue.empty():
            command = command_queue.get()
            if command == "EXIT":
                print("Global command received: Exiting game loop.")
                break

def main():
    input_thread = Thread(target=start_listening, daemon=True)
    input_thread.start()

    command_thread = Thread(target=process_global_commands, daemon=True)
    command_thread.start()

    try:
        main_game_loop()
    except KeyboardInterrupt:
        print("Game interrupted.")
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    main()