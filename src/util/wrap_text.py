import textwrap

def wrap_text(text, width):
    """Quebra o texto para caber na largura do terminal."""
    return textwrap.wrap(text, width)
