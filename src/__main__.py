from pynput import keyboard
from destinations.prismeer import city_menu
from destinations.prismeer.city import City
from characters.hero import Hero

comando = []
main_character = Hero()
prismeer = City()

def tecla_pressionada(key):
    global comando

    try:
        if key == keyboard.Key.enter:
            input_usuario = ''.join(comando).strip().upper()
            comando = []  

            if input_usuario == "P":
                print("You arrived at Prismeer!\n")
                city_menu(prismeer, main_character)
            else:
                print("P -- Prismeer")

        elif hasattr(key, 'char') and key.char is not None:
            comando.append(key.char)  
        elif key == keyboard.Key.backspace:
            if comando:
                comando.pop()  
    except Exception as e:
        print(f"Erro ao processar a tecla: {e}")

def tecla_soltada(key):
    if key == keyboard.Key.esc:
        print("Encerrando o programa...")
        return False  

with keyboard.Listener(on_press=tecla_pressionada, on_release=tecla_soltada) as listener:
    print("Pressione as teclas e aperte Enter para enviar. (ESC para sair)")
    print("P -- Prismeer")

    listener.join() 