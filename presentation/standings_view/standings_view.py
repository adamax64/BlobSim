from math import ceil
import time
from typing import List
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

from domain.dtos.grandmaster_standings_dto import GrandmasterStandingsDTO
from domain.dtos.league_dto import LeagueDto
from domain.dtos.standings_dto import StandingsDTO
from domain.sim_data_service import get_sim_time
from domain.standings_service import get_standings, get_grandmaster_standings
from domain.utils.league_utils import get_number_of_rounds_by_size
from domain.utils.sim_time_utils import get_season
from presentation.constants import KEY_ESCAPE, KEY_LEFT, KEY_RIGHT
from presentation.utils import capture_keypress, color_by_position


def show_standings_view(live: Live, league: LeagueDto | None):
    current_season = get_season(get_sim_time())
    season = _get_eon_start(current_season) if league is None else current_season
    step = 4 if league is None else 1

    standing_records = _get_standings_by_league(season, league, current_season)

    def render():
        if league is None:
            return render_eon(standing_records, int(season / 4) + 1)
        else:
            return render_season(standing_records, league, season, current_season)

    live.update(render(), refresh=True)

    while True:
        key = capture_keypress()

        if key == KEY_LEFT and season + step <= current_season:
            season += step
            standing_records = _get_standings_by_league(season, league, current_season)
            live.update(render(), refresh=True)
            time.sleep(0.1)
        elif key == KEY_RIGHT and season - step >= 1:
            season -= step
            standing_records = _get_standings_by_league(season, league, current_season)
            live.update(render(), refresh=True)
            time.sleep(0.1)
        elif key == KEY_ESCAPE:
            time.sleep(0.1)
            break


def render_season(standing_records: List[StandingsDTO], league: LeagueDto, season: int, current_season: int, is_summary: bool = False):
    if len(standing_records) == 0:
        return Panel(f'No data found for {league.name} season {str(season)}', title='No standings', title_align='left')

    table = Table(
        title=(
            f'Season has ended for {league.name}. Press any key to continue'
            if is_summary
            else 'Press Left and Right Arrows to navigate between seasons or Escape to return'
        )
    )

    table.add_column('#', justify='center')
    table.add_column('Name')
    num_of_rounds = (
        len(standing_records[0].results)
        if not season == current_season
        else get_number_of_rounds_by_size(league.field_size)
    )
    is_ended = num_of_rounds == len(standing_records[0].results)
    for i in range(num_of_rounds):
        table.add_column(f'R{i + 1}', justify='center')

    table.add_column('Sum', justify='center')

    for i, standing in enumerate(standing_records):
        rounds = _get_results_list(standing.results, num_of_rounds)
        position = i + 1
        table.add_row(
            color_by_position(position, position) if is_ended else str(position),
            color_by_position(position, standing.name) if is_ended else (
                f"[orange4]{standing.name}[/orange4]" if standing.is_contract_ending else standing.name
            ),
            *rounds,
            color_by_position(position, standing.total_points) if is_ended else str(standing.total_points)
        )
        if position == ceil(len(standing_records) / 2):
            table.add_section()

    title = (
        f'Congratulations for {standing_records[0].name} for winning!'
        if is_summary
        else f'{league.name} standings for season {str(season)}'
    )
    return Panel(table, title=title, title_align='left')


def render_eon(standing_records: List[GrandmasterStandingsDTO], eon: int | None):
    is_summary = eon is None
    table = Table(
        title=(
            'Eon is ended for the top league. Press any key to continue'
            if is_summary
            else 'Press Left and Right Arrows to navigate between eons or Escape to return'
        )
    )

    table.add_column('#', justify='center')
    table.add_column('Name')
    table.add_column('Championships', justify='center')
    table.add_column('Golds', justify='center')
    table.add_column('Silvers', justify='center')
    table.add_column('Bronzes', justify='center')
    table.add_column('Points', justify='center')

    for i, standing in enumerate(standing_records):
        table.add_row(
            str(i + 1),
            standing.name,
            str(standing.championships),
            str(standing.gold),
            str(standing.silver),
            str(standing.bronze),
            str(standing.points)
        )

    title = (
        f'Congratulations for {standing_records[0].name} for winning and becoming the new grandmaster!'
        if is_summary
        else f'Grandmaster standings for eon {str(eon)}'
    )
    return Panel(table, title=title, title_align='left')


def _get_standings_by_league(
    season: int, league: LeagueDto | None, current_season: int
) -> List[StandingsDTO] | List[GrandmasterStandingsDTO]:
    return get_grandmaster_standings(season, current_season) if league is None else get_standings(league.id, season, current_season)


def _get_results_list(results, num_of_rounds) -> List[str]:
    str_list = [color_by_position(result.position, result.points) for result in results]
    return str_list + [''] * (num_of_rounds - len(str_list))


def _get_eon_start(current_season: int) -> int:
    season = current_season - (current_season % 4 if current_season % 4 > 1 else 4)
    return season if season > 0 else 1
