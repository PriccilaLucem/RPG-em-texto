import curses

def display_message(stdscr: curses.window, message: str, delay: int = 1000) -> None:
    """
    Limpa a tela, exibe uma mensagem e espera um período de tempo opcional.

    Args:
        stdscr (curses.window): Janela de interface.
        message (str): Mensagem a ser exibida.
        delay (int): Tempo de espera em milissegundos.
    """
    stdscr.clear()
    stdscr.addstr(message + "\n")
    stdscr.refresh()
    curses.napms(delay)