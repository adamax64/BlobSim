import time
from rich.live import Live

from domain.championship_service import end_eon_if_over, end_season_if_over
from domain.competition_service import load_competition_data
from domain.dtos.event_dto import EventDto, EventTypeDto
from presentation.competition_view.endurance_race_view import show_endurance_race_view
from presentation.competition_view.quartered_high_jump_view import show_quartered_high_jump_view
from presentation.standings_view.standings_view import render_eon, render_season
from presentation.utils import capture_keypress


def show_competition_view(live: Live):
    event: EventDto = load_competition_data()
    tick = len(event.actions)
    tick = max(action.tick for action in event.actions) if len(event.actions) > 0 else 0
    field_size = event.league.field_size

    if event.type == EventTypeDto.ENDURANCE_RACE:
        show_endurance_race_view(live, event, tick, field_size)
    else:
        show_quartered_high_jump_view(live, event, tick, field_size)

    _check_and_render_season_end(live, event)


def _check_and_render_season_end(live: Live, event: EventDto):
    standings = end_season_if_over(event.league, event.season)
    if standings is not None:
        live.update(render_season(standings, event.league, event.season, event.season, True), refresh=True)
        capture_keypress()
        time.sleep(0.1)
    grandmaster_standings = end_eon_if_over(event.season, event.league)
    if grandmaster_standings is not None:
        live.update(render_eon(grandmaster_standings), refresh=True)
        capture_keypress()
        time.sleep(0.1)
