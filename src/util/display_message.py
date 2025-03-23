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
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    message = message[:width - 1]  

    message_x = (width - len(message)) // 2
    message_y = height // 2

    if message_y < 0: 
        message_y = 0
    if message_x < 0:  
        message_x = 0

    stdscr.attron(curses.color_pair(1))
    stdscr.border()
    stdscr.attroff(curses.color_pair(1))

    stdscr.addstr(message_y, message_x, message, color_pair)
    stdscr.refresh()
    curses.napms(delay)



def draw_menu(stdscr, title, options, selected_index, next = ""):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Título
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Opções normais
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Opção selecionada
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Rodapé
    
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1))
    stdscr.border()
    stdscr.attroff(curses.color_pair(1))

    # Exibir título centralizado
    title_x = (width - len(title)) // 2
    stdscr.addstr(2, title_x, title, curses.color_pair(1) | curses.A_BOLD)

    # Exibir opções do menu
    start_y = (height - len(options)) // 2
    for i, option in enumerate(options):
        option_x = (width - len(option)) // 2
        if i == selected_index:
            curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)  # Vermelho sobre fundo preto
            stdscr.addstr(start_y + i, option_x, option, curses.color_pair(7) | curses.A_BOLD)
        else:
            stdscr.addstr(start_y + i, option_x, option, curses.color_pair(1))
    
    # Exibir rodapé com instruções
    footer_text = next if next else  "Use ↑/↓ to navigate, ENTER to select" 
    footer_x = (width - len(footer_text)) // 2
    stdscr.addstr(height - 2, footer_x, footer_text, curses.color_pair(1) | curses.A_BOLD)
    
    stdscr.refresh()

def draw_menu_with_history(stdscr, title, history_text, options, selected_index):
    """
    Desenha um menu na tela com um título, texto de histórico, opções e destaque na opção selecionada.

    Args:
        stdscr (curses.window): Janela de interface.
        title (str): Título do menu.
        history_text (str): Texto de histórico a ser exibido.
        options (list): Lista de opções do menu.
        selected_index (int): Índice da opção selecionada.
    """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Título
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Opções normais
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Opção selecionada
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Rodapé
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)  # Vermelho sobre fundo preto

    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1))
    stdscr.border()
    stdscr.attroff(curses.color_pair(1))

    # Exibir título centralizado
    title_x = (width - len(title)) // 2
    stdscr.addstr(2, title_x, title, curses.color_pair(1) | curses.A_BOLD)

    # Exibir texto de histórico centralizado
    history_lines = history_text.split('\n')  # Divide o texto em linhas
    history_start_y = (height - len(options) - len(history_lines)) // 2

    for i, line in enumerate(history_lines):
        line_x = (width - len(line)) // 2
        stdscr.addstr(history_start_y + i, line_x, line, curses.color_pair(2))

    # Exibir opções do menu
    options_start_y = history_start_y + len(history_lines) + 1  # Espaço entre o histórico e as opções
    for i, option in enumerate(options):
        option_x = (width - len(option)) // 2
        if i == selected_index:
            stdscr.addstr(options_start_y + i, option_x, option, curses.color_pair(7) | curses.A_BOLD)
        else:
            stdscr.addstr(options_start_y + i, option_x, option, curses.color_pair(1))

    # Exibir rodapé com instruções
    stdscr.refresh()

def display_message_log(stdscr: curses.window, message_log: list):
    """
    Exibe o log de mensagens na parte inferior da tela, aplicando as cores corretas.
    """
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Título

    height, width = stdscr.getmaxyx()

    stdscr.attron(curses.color_pair(1))
    stdscr.border()
    stdscr.attroff(curses.color_pair(1))

    # Limpa a área do log para evitar sobreposição
    log_start_line = max(6, height - len(message_log) - 1)
    for y in range(log_start_line, height - 1):
        stdscr.move(y, 0)  # Move o cursor para a linha
        stdscr.clrtoeol()  # Limpa a linha

    # Exibe apenas as mensagens que cabem na tela
    visible_messages = message_log[-(height - log_start_line - 1):]

    # Exibe as mensagens com as cores correspondentes
    for idx, (msg, color) in enumerate(visible_messages):
        line = log_start_line + idx
        if line < height - 1:  # Evita escrever fora da tela
            stdscr.addstr(line, 0, msg, color)  # Aplica a cor correta

    stdscr.refresh()  # Atualiza a tela para exibir as mudanças