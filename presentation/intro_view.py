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
    if width >= 31 and height >= 17:
        vertical_padding = _get_vertical_padding(height)

        for _ in range(vertical_padding):
            print()

        logo_padding = ' ' * _get_padding_size(width, 31)
        logo = LOGO.split('\n')
        for line in logo:
            print(f'{logo_padding}{line}')

        for _ in range(vertical_padding):
            print()

    title_padding = ' ' * _get_padding_size(width, 24)
    print(f'{title_padding}BLOB CHAMPIONSHIP SYSTEM')
    version_padding = ' ' * _get_padding_size(width, 4)
    print(f'{version_padding}v1.2')
    copyright_padding = ' ' * _get_padding_size(width, 22)
    print(f'{copyright_padding}by Adamax-works © 2025')
    disclaimer_padding = ' ' * _get_padding_size(width, 120) if width > 120 else ''
    print(f'{disclaimer_padding}Disclaimer: this is a simulation of fictional creatures, '
          f'every name matching with real persons are just mere coincidence')
    print()
    start_padding = ' ' * _get_padding_size(width, 22)
    print(f'{start_padding}Press any key to start')
    capture_keypress()
    clear_console()


def _get_vertical_padding(console_height: int) -> int:
    padding = int((console_height - 18) / 2)
    return min(padding, 4)


def _get_padding_size(console_width: int, text_length: int) -> int:
    return int((console_width - text_length) / 2)
