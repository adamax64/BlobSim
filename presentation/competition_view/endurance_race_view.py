from collections import defaultdict
import random
import time
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

from domain.competition_service import create_action, save_event_results
from domain.dtos.action_dto import ActionDto
from domain.dtos.event_dto import EventDto
from domain.dtos.event_record_dto import RaceEventRecordDto
from domain.dtos.save_action_dto import SaveActionDto
from domain.utils.league_utils import get_race_duration_by_size
from presentation.constants import KEY_ESCAPE, KEY_SPACE
from presentation.utils import capture_keypress, color_by_position, get_text_by_key


def show_endurance_race_view(live: Live, event: EventDto, tick: int, field_size: int):
    event_duration = get_race_duration_by_size(field_size)

    event_records = _get_event_records(event)

    def render(status_text: str = "Press Space to continue", loading: int = None, ended=False):
        table = Table(
            title=status_text,
            caption=f"Tick: {tick}/{event_duration}" if loading is None else "." * loading,
            caption_justify="left" if loading is not None else "center"
        )

        table.add_column("#")
        table.add_column("Name")
        table.add_column("Distance run", justify="center")
        table.add_column("Leader (distance)", justify="center")
        table.add_column("Interval (distance)", justify="center")

        for index, record in enumerate(event_records):
            position = index + 1
            previous_position = record.previous_position

            # delta, cumulative_delta = _calculate_delta_times(record, event_records, index) TODO: refine the time delta calculation

            distance_run = f"{round(record.distance_records[-1], 1)}" if len(record.distance_records) > 0 else "0.0"
            distance_leader = (
                f"{round(event_records[0].distance_records[-1] - record.distance_records[-1], 2)}"
                if len(record.distance_records) > 0 else "0.0"
            )
            distance_interval = (
                f"{round(event_records[index - 1].distance_records[-1] - record.distance_records[-1], 3)}"
                if index > 0 and len(record.distance_records) > 0 else "0.0"
            )

            table.add_row(
                _display_data(position, previous_position, ended, position),
                _display_data(position, previous_position, ended, record.blob.name),
                _display_data(position, previous_position, ended, distance_run),
                _display_data(position, previous_position, ended, f"{distance_leader if position > 1 else '-'}"),
                _display_data(position, previous_position, ended, f"{distance_interval if position > 1 else '-'}")
            )

            record.previous_position = position

        return Panel(
            table,
            title=f"{event.league.name} Season {event.season} Round {event.round}, {get_text_by_key(event.type)}",
            title_align="left"
        )

    live.update(render(), refresh=True)

    while True:
        key = capture_keypress()

        if key == KEY_SPACE:
            if tick > event_duration:
                time.sleep(0.1)
                save_event_results(event=event, event_records=event_records)
                live.update(render("Competition is over. Press any key to return", ended=True), refresh=True)
                capture_keypress()
                time.sleep(0.1)
                break

            for i in range(10):
                live.update(render("progressing time...", loading=i+1), refresh=True)
                time.sleep(0.1)

            for record in event_records:
                score = record.blob.strength * random.random() * 10
                create_action(action=SaveActionDto(event.id, tick, record.blob.id, score))
                previous_distance = record.distance_records[-1] if len(record.distance_records) > 0 else 0
                record.distance_records.append(previous_distance + score)
                _calculate_time_if_crossed_detection_point(record, tick)

            tick += 1
            event_records.sort(key=_sort_lambda(), reverse=True)
            live.update(render(), refresh=True)

        if key == KEY_ESCAPE:
            time.sleep(0.1)
            break


def _get_event_records(event: EventDto) -> list[RaceEventRecordDto]:
    actions_by_tick = defaultdict(list[ActionDto])
    for action in event.actions:
        if action.tick not in actions_by_tick:
            actions_by_tick[action.tick] = []
        actions_by_tick[action.tick].append(action)

    competitors = {competitor.id: RaceEventRecordDto(blob=competitor) for competitor in event.competitors}

    for tick in actions_by_tick.keys():
        actions = actions_by_tick[tick]
        for action in actions:
            competitor = competitors[action.blob_id]
            previous_distance = competitor.distance_records[-1] if len(competitor.distance_records) > 0 else 0
            competitor.distance_records.append(previous_distance + action.score)
            _calculate_time_if_crossed_detection_point(competitor, tick)

    sorted_competitors = sorted(competitors.values(), key=_sort_lambda(), reverse=True)
    for i, competitor in enumerate(sorted_competitors):
        competitor.previous_position = i + 1
    return sorted_competitors


def _calculate_time_if_crossed_detection_point(competitor: RaceEventRecordDto, tick: int):
    distance_n_1 = competitor.distance_records[-2] if len(competitor.distance_records) > 1 else 0
    distance_n = competitor.distance_records[-1]
    detection_points = int(distance_n) - int(distance_n_1)
    if detection_points == 0:
        return

    for dp in range(int(distance_n_1) + 1, int(distance_n) + 1):
        velocity_n = distance_n - distance_n_1
        distance_to_dp = dp - distance_n_1
        competitor.time_records.append(tick + distance_to_dp / velocity_n)


def _calculate_delta_times(current: RaceEventRecordDto, event_records: list[RaceEventRecordDto], index: int) -> tuple[float, float]:
    detection_point = len(current.time_records) - 1
    time = current.time_records[detection_point] if len(current.time_records) > 0 else 0
    delta = (
        time - event_records[index - 1].time_records[detection_point]
        if index > 0 and len(current.time_records) > 0 else None
    )
    cumulative_delta = (
        time - event_records[0].time_records[detection_point]
        if index > 0 and len(current.time_records) > 0 else None
    )
    return delta, cumulative_delta


def _display_data(position: int, previous_position: int, ended: bool, data) -> str:
    if ended:
        return color_by_position(position, data)
    if position < previous_position:
        return f"[green]{str(data)}[/green]"
    if position > previous_position:
        return f"[yellow]{str(data)}[/yellow]"
    return str(data)


def _sort_lambda():
    return lambda x: x.distance_records[-1] if len(x.distance_records) > 0 else 0
