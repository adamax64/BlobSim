import random
import time
from typing import List, Tuple
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

from domain.championship_service import end_eon_if_over, end_season_if_over
from domain.competition_service import create_action, load_competition_data, save_event_results
from domain.dtos.event_dto import EventDto
from domain.dtos.save_action_dto import SaveActionDto
from domain.dtos.event_record_dto import ScoreDto, QuarteredEventRecordDto
from presentation.competition_view.utils import (
    display_blob, display_score, get_eliminations, get_quarter_ends, is_eliminated
)
from presentation.constants import KEY_ESCAPE, KEY_SPACE
from presentation.standings_view.standings_view import render_eon, render_season
from presentation.utils import capture_keypress, color_by_position, get_text_by_key


def show_competition_view(live: Live):
    event: EventDto = load_competition_data()
    tick = len(event.actions)
    field_size = event.league.field_size
    quarter_ends = get_quarter_ends(field_size, event.type)
    quarter = _get_current_quarter(quarter_ends, tick)

    event_records = _get_event_records(event, quarter_ends)

    current_score: ScoreDto = None

    def render(status_text: str = 'Press Space to continue', active_blob_id=None, ended=False):
        table = Table(title=status_text)

        table.add_column('#')
        table.add_column('Name')
        table.add_column('Q1', justify='center', min_width=5)
        table.add_column('Q2', justify='center', min_width=5)
        table.add_column('Q3', justify='center', min_width=5)
        table.add_column('Q4', justify='center', min_width=5)

        for index, record in enumerate(event_records):
            position = index + 1
            eliminated = is_eliminated(min(quarter, 4), field_size, position) and not ended
            scores = [display_score(record.quarters[i], eliminated) for i in range(4)]
            table.add_row(
                color_by_position(position, position) if ended else (
                    f'[bright_black]{str(position)}[/bright_black]' if eliminated else str(position)
                ),
                color_by_position(position, record.blob.name) if ended else display_blob(
                    record.blob, active_blob_id, eliminated
                ),
                *scores
            )

        return Panel(
            table,
            title=f'{event.league.name} Season {event.season} Round {event.round}, {get_text_by_key(event.type)}',
            title_align='left'
        )

    live.update(render(), refresh=True)

    while True:
        key = capture_keypress()

        if key == KEY_SPACE:
            if current_score is not None:
                current_score.personal_best = False
                current_score.latest_score = None

            if quarter > 4:
                time.sleep(0.1)
                save_event_results(event=event, event_records=event_records)
                live.update(render('Competition is over. Press any key to return', ended=True), refresh=True)
                capture_keypress()
                time.sleep(0.1)
                _check_and_render_season_end(live, event)
                break

            (index, end_of_quarter) = _get_quarter_data(quarter_ends, tick, quarter, field_size)
            current_blob = event_records[index].blob
            current_blob_id = current_blob.id

            current_score = event_records[index].quarters[quarter - 1]

            current_score.scoring_progress = 1
            live.update(render('Blob is currently scoring', current_blob_id), refresh=True)
            time.sleep(0.5)

            current_score.scoring_progress = 2
            live.update(render('Blob is currently scoring', current_blob_id), refresh=True)
            time.sleep(0.5)

            current_score.scoring_progress = 3
            live.update(render('Blob is currently scoring', current_blob_id), refresh=True)
            time.sleep(0.5)

            current_score.scoring_progress = None
            score = current_blob.strength * random.random()
            create_action(action=SaveActionDto(event.id, tick, current_blob.id, score))
            _assing_score(current_score, score)

            tick += 1

            event_records.sort(key=_sort_lambda(quarter - 1), reverse=True)

            if end_of_quarter:
                event_records[0].quarters[quarter - 1].best = True
                quarter += 1

            live.update(render(), refresh=True)

        if key == KEY_ESCAPE:
            time.sleep(0.1)
            break


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


def _assing_score(scoreDto: ScoreDto, actual_score: int):
    if scoreDto.score is None:
        scoreDto.score = actual_score
        scoreDto.personal_best = True
    else:
        if scoreDto.score < actual_score:
            scoreDto.score = actual_score
            scoreDto.personal_best = True
        else:
            scoreDto.latest_score = actual_score


def _get_current_quarter(quarter_ends: List[int], tick: int) -> int:
    for i, end in enumerate(quarter_ends):
        if tick < end:
            return i + 1
    return 5


def _get_quarter_data(quarter_ends: List[int], tick: int, quarter: int, field_size: int) -> Tuple[int, bool]:
    end_of_quarter = tick + 1 in quarter_ends
    if quarter == 1:
        return tick % field_size, end_of_quarter
    else:
        current_field_size = field_size - (quarter - 1) * get_eliminations(field_size)
        quarter_tick = tick - quarter_ends[quarter - 2]
        return quarter_tick % current_field_size, end_of_quarter


def _get_event_records(event: EventDto, quarter_ends: List[int]):
    records = {blob.id: QuarteredEventRecordDto(blob, [ScoreDto(), ScoreDto(), ScoreDto(), ScoreDto()]) for blob in event.competitors}

    quarter = 1
    for action in event.actions:
        quarter = _get_current_quarter(quarter_ends, action.tick)
        score = records[action.blob_id].quarters[quarter - 1]
        if score.score is None or score.score < action.score:
            score.score = action.score

    result_records = list(records.values())

    if len(event.actions) > 0:
        current_quarter = _get_current_quarter(quarter_ends, len(event.actions))
        for q in range(current_quarter - 1):
            result_records.sort(key=_sort_lambda(q), reverse=True)
            result_records[0].quarters[q].best = True
        if current_quarter == quarter:
            result_records.sort(key=_sort_lambda(quarter - 1), reverse=True)

    return result_records


def _sort_lambda(index: int):
    return lambda x: (
                    x.quarters[index].score is not None,
                    x.quarters[index].score if x.quarters[index] is not None else -1
                )
