import time
from rich.live import Live
from rich.prompt import Prompt

from domain.blob_service import create_blob


def show_create_blob(live: Live):
    live.update('Creating new blob')
    while True:
        time.sleep(0.1)
        name = Prompt.ask('Enter name for new blob')
        name = name.strip()
        if len(name.split()) == 2:
            create_blob(name=name)
            break
        else:
            live.update('Invalid name. Please enter a name with two words.')
