from destinations.prismeer.city import city
from characters.hero import hero

def city_menu(prismeer: city, main_character: hero) -> None:
    inn = prismeer.inn
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
                inn.pass_the_night(main_character)
            case "B":
                visit_city_center(prismeer, main_character)
            case "E":
                print("Leaving Prismeer...\n")
                break
            case _:
                print("Invalid choice. Try again.\n")


def visit_city_center(prismeer: city, main_character: hero) -> None:
    count_armor_speech = 1
    while True:
        print(
            """
            Welcome to the city center:
            A - Visit the armor shop
            W - Visit the weapon shop
            E - Exit to city menu
            """
        )
        center_key = input("Where do you want to go? ").strip().upper()
        match center_key:
            case "A":
                prismeer.downtown.armor_shop.shop_interactions(main_character)
            case "W":
                print(prismeer.downtown.weapon_shop.seller.speech(0))
                count_armor_speech += 1
            case "E":
                print("Returning to city menu...\n")
                break
            case _:
                print("Invalid choice. Try again.")
