from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich import box
import time

from domain.sim_data_service import get_sim_time, is_blob_created, is_unconcluded_event_today
from domain.utils.sim_time_utils import is_season_start
from presentation.blobs_view import show_blobs_view
from presentation.calendar_view import show_calendar_view
from presentation.competition_view.competition_view import show_competition_view
from presentation.constants import KEY_DOWN, KEY_ENTER, KEY_ESCAPE, KEY_UP
from presentation.create_blob_view import show_create_blob
from presentation.simulate_view import show_simulation_progress
from presentation.standings_view.league_selector_view import show_league_selector_view
from presentation.utils import capture_keypress, format_sim_time


ESCAPE_KEY = 27
ENTER_KEY = ord('\n')


class Option():
    def __init__(self, title, callback):
        self.title = title
        self.callback = callback


def show_main_menu():
    console = Console()

    generic_options = [
        Option('View Blobs', show_blobs_view),
        Option('View standings', show_league_selector_view),
        Option('View Calendar', show_calendar_view)
        # Option('View previous events', None)
    ]
    current_row = 0

    options = generic_options
    current_date = get_sim_time()

    def render_menu():
        table = Table(box=box.MINIMAL)
        table.add_column(print_status_text(get_event_specific_options().keys(), current_date))

        for idx, option in enumerate(options):
            if idx == current_row:
                table.add_row(f" -> [cyan]{option.title}[/cyan]")
            else:
                table.add_row(f"    {option.title}")

        return Panel(table, title=f'Curernt date: {format_sim_time(current_date)}', title_align="left")

    with Live(render_menu(), auto_refresh=False, console=console, screen=True) as live:
        options_dict = get_event_specific_options()

        options = list(options_dict.values())
        [options.append(gen_option) for gen_option in generic_options]

        live.update(render_menu(), refresh=True)

        while True:
            current_date = get_sim_time()
            options_dict = get_event_specific_options()

            options = list(options_dict.values())
            [options.append(gen_option) for gen_option in generic_options]

            live.update(render_menu(), refresh=True)

            key = capture_keypress()

            if key == KEY_UP and current_row > 0:
                current_row -= 1
                live.update(render_menu(), refresh=True)
                time.sleep(0.1)
            elif key == KEY_DOWN and current_row < len(options) - 1:
                current_row += 1
                live.update(render_menu(), refresh=True)
                time.sleep(0.1)
            elif key == KEY_ENTER:
                if options[current_row].callback:
                    time.sleep(0.1)
                    options[current_row].callback(live)
                live.update(render_menu(), refresh=True)
            elif key == KEY_ESCAPE:
                break


def get_event_specific_options() -> Dict[str, Option]:
    options = {}

    if is_unconcluded_event_today():
        options['EVENT'] = Option('Proceed to event', show_competition_view)
    if is_blob_created():
        options['BLOB_CREATED'] = Option('Create new blob', show_create_blob)
    if len(options) == 0:
        options['CONTINUE'] = Option('Proceed to next day', show_simulation_progress)

    return options


def print_status_text(option_keys: List[str], current_date: int) -> str:
    if 'EVENT' in option_keys:
        return '[green]There is a championship event today![/green]'
    elif 'BLOB_CREATED' in option_keys:
        return '[blue]A new blob has been created![/blue]'
    elif is_season_start(current_date):
        return '[yellow]A new season has started![/yellow]'
    else:
        return 'Nothing special happening today'
