def global_commands():
    return"""
    S - View Status"""
          
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
    {global_commands()}
    T - Talk to the seller
    S - Buy items
    E - Leave the shop
    """

def cave_commands():
    return f"""
    {global_commands()}
    Enter - Enter the cave
    E - Go to Prismeer's surroundings
    """
def mine_cave_commands():
    return f"""
    {global_commands()}
    M - Mine some ores
    E - Leave to outside the cave
    """
def inside_cave_commands():
    return f"""
    {global_commands()}
    1 - Talk to first brother
    2 - Talk to second brother
    3 - Scavenge Owlbear
    E - Go to outside the cave
    """