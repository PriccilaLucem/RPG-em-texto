from characters.hero import hero
from destinations.prismeer import city
from destinations.prismeer import city_menu

if "__main__":
    
    main_character = hero()
    prismeer = city()
       
    while True:
        print(
            "C - City \n"
        )
        key = input("Type your action \n").capitalize()
        match key:
            case "C":
                print("You arrived at Prismeer!\n")
                city_menu(prismeer, main_character)
            case _:
                print("Invalid action. Try again.\n")
                