from dataclasses import dataclass

from domain.dtos.event_dto import EventTypeDto
from domain.dtos.sim_time_dto import SimTimeDto


@dataclass
class CalendarDto:
    date: SimTimeDto
    league_name: str
    is_concluded: bool
    event_type: EventTypeDto
    is_next: bool
    is_current: bool
