from dataclasses import dataclass

from domain.dtos.event_dto import EventTypeDto
from domain.dtos.sim_time_dto import SimTimeDto


@dataclass
class SeasonCompetitionDto:
    date: SimTimeDto
    league_name: str
    round: int
    event_type: EventTypeDto
