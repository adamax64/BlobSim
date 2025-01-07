import time
import tkinter as tk
from tkinter import simpledialog
from rich.live import Live

from domain.blob_service import create_blob
from domain.exceptions.name_occupied_exception import NameOccupiedException
from domain.naming_service import save_name_suggestion
from presentation.utils import capture_keypress


def show_create_blob(live: Live):
    _blob_name_prompt(live, True)


def show_add_name_suggestion(live: Live):
    _blob_name_prompt(live, False)


def _blob_name_prompt(live: Live, create: bool):
    root = tk.Tk()
    root.withdraw()

    prompt = 'Enter name for new blob' if create else 'Enter name suggestion'

    while True:
        time.sleep(0.1)
        live.update(prompt, refresh=True)

        name = simpledialog.askstring('Blob creaton' if create else 'Name suggestion', prompt)

        if name is None:
            time.sleep(0.1)
            break
        if len(name.split()) == 2:
            if create:
                create_blob(name=name)
            else:
                try:
                    save_name_suggestion(name=name)
                except NameOccupiedException:
                    prompt = 'This name already exists in the name suggestions list. Please enter another name'
                    continue

            response_text = f'Blob "{name}" created successfully!' if create else 'Name suggastion saved.'
            live.update(f'{response_text} Press any key to continue', refresh=True)
            capture_keypress()
            break
        else:
            prompt = 'Invalid name. Please enter a name with two words'
