from typing import List

from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_record_dto import ScoreDto
from domain.dtos.event_dto import EventTypeDto


def display_score(scoreDto: ScoreDto, is_eliminated: bool = False) -> str:
    if scoreDto.score is None:
        return ''
    if scoreDto.latest_score is not None:
        return f'[yellow]{str(round(scoreDto.latest_score, 3))}[/yellow]'

    score = round(scoreDto.score, 3)
    if scoreDto.personal_best:
        return f'[green]{str(score)}[/green]'
    if scoreDto.best:
        return f'[grey100]{str(score)}[/grey100]'
    if is_eliminated:
        return f'[bright_black]{str(score)}[/bright_black]'

    return str(score)


def display_blob(blob: BlobCompetitorDto, active_blob_id: int, is_eliminated: bool = False) -> str:
    if is_eliminated:
        return f'[bright_black]{blob.name}[/bright_black]'
    if blob.id == active_blob_id:
        return f'[cyan]{blob.name}[/cyan]'
    else:
        return blob.name


def is_eliminated(quarter: int, field_size: int, position: int) -> int:
    eliminations = (quarter - 1) * get_eliminations(field_size)
    threshold = field_size - eliminations
    return position > threshold


def get_quarter_ends(field_size: int, event_type: EventTypeDto) -> List[int]:
    eliminations = get_eliminations(field_size)
    multiplyer = 1
    if event_type == EventTypeDto.QUARTERED_TWO_SHOT_SCORING:
        multiplyer = 2
    return [
        multiplyer * (field_size),
        multiplyer * (2 * field_size - eliminations),
        multiplyer * (3 * field_size - 3 * eliminations),
        multiplyer * (4 * field_size - 6 * eliminations)
    ]


def get_eliminations(field_size: int) -> int:
    return int((field_size - 3) / 3) if field_size < 15 else field_size / 4
