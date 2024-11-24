def global_commands():
    return"""
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

def billboard_commands():
    return f"""
    {global_commands()}
    Q - Take a quest
    E - Exit Billboard
    N - Notes   
    """

def shop_commands():
    return f"""
    You entered the shop. What would you like to do?"
    T - Talk to the seller
    B - Buy items
    E - Leave the shop
    """