from dataclasses import dataclass

from domain.dtos.event_dto import EventTypeDto
from domain.dtos.sim_time_dto import SimTimeDto
from domain.dtos.translations_dto import TranslationsDto


@dataclass
class CalendarDto:
    date: SimTimeDto
    league_name: list[TranslationsDto]
    league_level: int
    round: int
    is_concluded: bool
    event_type: EventTypeDto
    is_next: bool
    is_current: bool
    event_id: int | None = None
