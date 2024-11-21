from destinations.prismeer.city import city
from characters.hero import hero

def city_menu(prismeer: city, main_character: hero) -> None:
    while True:
        print(
            """
            Choose your action:
            Q - Take a quest
            I - Rest at the inn
            B - Go to the center
            E - Exit the city
            """
        )
        city_key = input("Where do you want to go? ").capitalize()
        match city_key:
            case "Q":
                print("You head to the billboard to take a quest.\n")
            case "I":
                print("You entered the inn would you like to take a rest? \n")
                print("""
                        Y - Yes \n
                        N - No
                      """)
                while True:
                    inn_input = input().capitalize()
                    match inn_input:
                        case "Y":
                            if(main_character.gold < prismeer.inn.cost):
                                prismeer.inn.pass_the_night(main_character)
                                print("You dont't have the gold!")

                        case "N":
                            break
                        case _:
                            print("Invalid choice. Try again")
            case "B":
                print("You walk to the bustling city center.\n")
            case "E":
                print("Leaving Prismeer...\n")
                break
            case _:
                print("Invalid choice. Try again.\n")
