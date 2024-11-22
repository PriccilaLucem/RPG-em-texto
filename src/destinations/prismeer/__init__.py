def city_menu(prismeer, main_character) -> None:
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
        city_key = input("Where do you want to go? ").strip().upper()
        match city_key:
            case "Q":
                print("You head to the billboard to take a quest.\n")
            case "I":
                print("You entered the inn. Would you like to rest?\n")
                print("Y - Yes\nN - No\n")
                while True:
                    inn_input = input().strip().upper()
                    match inn_input:
                        case "Y":
                            if main_character.gold < prismeer.inn.cost:
                                print("You don't have enough gold!")
                            else:
                                prismeer.inn.pass_the_night(main_character)
                                print("You rested at the inn.")
                            break
                        case "N":
                            break
                        case _:
                            print("Invalid choice. Try again.")
            case "B":
                print("You walk to the bustling city center.\n")
            case "E":
                print("Leaving Prismeer...\n")
                break
            case _:
                print("Invalid choice. Try again.\n")