from characters.hero import hero
    
if "__main__":
    loop_variable = True
    while loop_variable:
        key = input("Digite sua acao \n").capitalize()
        main_character = hero()
        print(main_character.__getattribute__("hp"))