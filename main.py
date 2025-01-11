import ctypes
import os
import sys

from domain.startup_service import startup
from presentation.intro_view import show_intro_view
from presentation.constants import APP_NAME
from presentation.main_menu_view import show_main_menu
from presentation.utils import clear_console


def set_window_icon():
    icon_path = "./assets/blob.ico"
    if os.name == 'nt':  # Check if the OS is Windows
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(icon_path)
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            hicon = ctypes.windll.user32.LoadImageW(0, icon_path, 1, 0, 0, 0x00000010)
            ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, hicon)


if __name__ == "__main__":
    os.system(f"title {APP_NAME}{' debug mode' if 'debug' in sys.argv else ''}")
    set_window_icon()
    startup()
    clear_console()
    show_intro_view()
    show_main_menu()
