import time
from typing import List
from rich.live import Live
from rich.table import Table

from domain.calendar_service import get_season_calendar
from domain.dtos.calendar_dto import CalendarDto
from presentation.utils import capture_keypress, format_sim_time_short, get_text_by_key, highlight_by_condition


def show_calendar_view(live: Live):
    calendar: List[CalendarDto] = get_season_calendar()

    table = Table(title='Season Calendar (press any key to return)', box=None, min_width=60)

    table.add_column()
    table.add_column('Date')
    table.add_column('League')
    table.add_column('Event Type')

    for i, event in enumerate(calendar):
        is_next = not event.is_concluded and (i == 0 or calendar[i - 1].is_concluded)
        table.add_row(
            '[cyan] -> [/cyan]' if is_next else '',
            highlight_by_condition(format_sim_time_short(event.date), is_next),
            highlight_by_condition(event.league_name, is_next),
            highlight_by_condition(get_text_by_key(event.event_type), is_next)
        )

    live.update(table, refresh=True)

    capture_keypress()
    time.sleep(0.1)
