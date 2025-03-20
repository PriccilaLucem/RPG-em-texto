def global_commands():
    return """
    M - Menu
    """
          
def game_init():
    return f"""
    {global_commands().strip()}
    P - Prismeer"""



def billboard_commands():
    return f"""
    Q - Exit Billboard
    F - Take a quest
    N - Notes   
    {global_commands().strip()}
    """


def cave_commands():
    return f"""
    Q - Go to Prismeer's surroundings
    E - Enter the cave
    {global_commands().strip()}
    """
