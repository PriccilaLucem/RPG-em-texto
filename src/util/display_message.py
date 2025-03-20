import curses

def display_message(stdscr: curses.window, message: str, delay: int = 1000, color_pair: int = 0) -> None:
    """
    Exibe uma mensagem na tela e espera um período de tempo opcional.

    Args:
        stdscr (curses.window): Janela de interface.
        message (str): Mensagem a ser exibida.
        delay (int): Tempo de espera em milissegundos.
        color_pair (int): Par de cores a ser usado (opcional).
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Ensure the message fits within the window width
    message = message[:width - 1]  # Truncate message if it's too long

    # Calculate position to center the message
    message_x = (width - len(message)) // 2
    message_y = height // 2

    # Make sure the message fits in the window
    if message_y < 0:  # Ensure the message Y-coordinate is valid
        message_y = 0
    if message_x < 0:  # Ensure the message X-coordinate is valid
        message_x = 0

    # Display the message on the screen
    stdscr.addstr(message_y, message_x, message, color_pair)
    stdscr.refresh()
    curses.napms(delay)


def draw_menu(stdscr: curses.window, title: str, options: list, selected_index: int):
    # Configurações de cores
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Título
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Opções normais
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Opção selecionada

    # Limpa a tela
    stdscr.clear()

    # Obtém as dimensões da tela
    height, width = stdscr.getmaxyx()

    # Desenha a borda ao redor da tela
    stdscr.border(0)

    # Centraliza o título
    title_x = (width - len(title)) // 2
    if title_x >= 0 and 2 < height:
        stdscr.addstr(2, title_x, title, curses.color_pair(1))

    # Desenha as opções do menu
    for i, option in enumerate(options):
        # Calculando a posição horizontal da opção
        option_x = (width - len(option)) // 2  # Centraliza a opção
        if option_x >= 0 and 5 + i < height:
            if i == selected_index:
                stdscr.addstr(5 + i, option_x, option, curses.color_pair(3))  # Opção selecionada
            else:
                stdscr.addstr(5 + i, option_x, option, curses.color_pair(2))  # Opções normais

    # Atualiza a tela
    stdscr.refresh()


def display_message_log(stdscr: curses.window, message_log: list):
    height, width = stdscr.getmaxyx()

    # Define a linha inicial para o log (parte inferior da tela)
    log_start_line = max(6, height - len(message_log) - 1)

    # Exibe apenas as mensagens que cabem na tela
    visible_messages = message_log[-(height - log_start_line - 1):]

    # Exibe as mensagens
    for idx, msg in enumerate(visible_messages):
        line = log_start_line + idx
        if line < height:  # Evita escrever fora da tela
            stdscr.addnstr(line, 0, str(msg), width - 1)  # Limita o texto ao tamanho da tela