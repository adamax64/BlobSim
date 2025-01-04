import os

from presentation.intro_view import show_intro_view
from presentation.constants import APP_NAME
from presentation.main_menu_view import show_main_menu
from presentation.utils import clear_console


if __name__ == "__main__":
    os.system(f'title {APP_NAME}')
    clear_console()
    show_intro_view()
    show_main_menu()
