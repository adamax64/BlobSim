from dataclasses import dataclass

from domain.dtos.event_dto import EventTypeDto
from domain.dtos.sim_time_dto import SimTimeDto
from domain.dtos.translations_dto import TranslationsDto


@dataclass
class CalendarDto:
    date: SimTimeDto
    round: int
    is_concluded: bool
    event_type: EventTypeDto
    is_next: bool
    is_current: bool
    league_name: list[TranslationsDto] | None = None
    league_level: int | None = None
    event_id: int | None = None
