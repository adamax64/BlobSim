from presentation.utils import capture_keypress, clear_console, get_console_height, get_console_width


LOGO = (
    '                              \n'
    '          ▄▄▄▄▄▄▄▄▄▄          \n'
    '      ▄▄▀▀          ▀▀▄▄      \n'
    '   ▄█▀                  ▀█▄   \n'
    ' █▀                        ▀█ \n'
    '█        █          █        █\n'
    '█                            █\n'
    '█                            █\n'
    '█                            █\n'
    ' ▀█▄                      ▄█▀ \n'
    '    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀    \n'
    '                              \n'
)


def show_intro_view():
    width = get_console_width()
    height = get_console_height()
    if width >= 31 and height >= 18:
        vertical_padding = _get_vertical_padding(height)

        for _ in range(vertical_padding):
            print()

        logo_padding = ' ' * _get_padding_size(width, 31)
        logo = LOGO.split('\n')
        for line in logo:
            print(f'{logo_padding}{line}')

        for _ in range(vertical_padding):
            print()

    _print_text_centered("BLOB CHAMPIONSHIP SYSTEM", width)
    _print_text_centered("v1.2.5", width)
    _print_text_centered("by Adamax-works © 2025", width)
    _print_text_centered(
        "Disclaimer: this is a simulation of fictional creatures, every name matching with real persons, "
        "fictional characters from other franchises",
        width
    )
    _print_text_centered("or brands of products are just mere coincidence", width)
    print()
    _print_text_centered("Press any key to start", width)
    capture_keypress()
    clear_console()


def _print_text_centered(text: str, console_width: int):
    text_length = len(text)
    padding = ' ' * _get_padding_size(console_width, text_length) if console_width > text_length else ''
    print(f'{padding}{text}')


def _get_vertical_padding(console_height: int) -> int:
    padding = int((console_height - 18) / 2)
    return min(padding, 4)


def _get_padding_size(console_width: int, text_length: int) -> int:
    return int((console_width - text_length) / 2)
