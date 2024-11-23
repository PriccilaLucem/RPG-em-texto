from characters.hero import hero

class Inn:
    def __init__(self, cost: int) -> None:
        self.cost = cost
    
    def pass_the_night(self, main_character: hero) -> None:
        while True:
            print("Would you like to rest? (Y/N)")
            inn_choice = input().strip().upper()
            match inn_choice:
                case "Y":
                    if main_character.gold < self.cost:
                        print("You don't have enough gold!")
                    else:
                        main_character.gold -= self.cost
                        main_character.hp = main_character.max_hp
                        print(f"You rested at the inn. Remaining gold: {main_character.gold}")
                    break
                case "N":
                    print("You chose not to rest.\n")
                    break
                case _:
                    print("Invalid choice. Try again.")
