from dataclasses import dataclass

from domain.dtos.event_dto import EventTypeDto


@dataclass
class CalendarDto:
    date: int
    league_name: str
    is_concluded: bool
    event_type: EventTypeDto
