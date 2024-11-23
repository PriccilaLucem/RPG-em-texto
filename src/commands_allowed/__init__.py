def global_commands():
    return"""
    EXIT - Quit the game
    B - View Backpack"""
          
def game_init():
    return f"""
    {global_commands()}
    P - Prismeer"""

def prismeer_commands():
    return f"""
    {global_commands()}
    Q - Take a quest
    I - Rest at the inn
    C - Go to the center
    E - Exit the city
    """
