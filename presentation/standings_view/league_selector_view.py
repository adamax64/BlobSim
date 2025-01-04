import time
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

from domain.league_service import get_all_real_leagues
from presentation.constants import KEY_DOWN, KEY_ENTER, KEY_ESCAPE, KEY_UP
from presentation.standings_view.standings_view import show_standings_view
from presentation.utils import capture_keypress


def show_league_selector_view(live: Live):
    leagues = get_all_real_leagues()
    current_row = 0

    def render():
        table = Table(title='Select league to view standings or press Escape to return', box=None, min_width=60)

        table.add_column()

        table.add_row(' -> [cyan]Grandmasters championship[/cyan]' if current_row == 0 else '    Grandmasters championship')
        for i, league in enumerate(leagues):
            table.add_row(f' -> [cyan]{league.name}[/cyan]' if i + 1 == current_row else f'    {league.name}')

        return Panel(table, title='Leagues Selector', title_align='left')

    live.update(render(), refresh=True)

    while True:
        key = capture_keypress()

        if key == KEY_UP and current_row > 0:
            current_row -= 1
            live.update(render(), refresh=True)
            time.sleep(0.1)
        elif key == KEY_DOWN and current_row < len(leagues):
            current_row += 1
            live.update(render(), refresh=True)
            time.sleep(0.1)
        elif key == KEY_ENTER:
            show_standings_view(live, leagues[current_row - 1] if current_row > 0 else None)
            live.update(render(), refresh=True)
            pass
        elif key == KEY_ESCAPE:
            time.sleep(0.1)
            break
