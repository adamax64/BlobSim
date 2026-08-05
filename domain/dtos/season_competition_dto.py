from dataclasses import dataclass

from domain.dtos.event_dto import EventTypeDto
from domain.dtos.sim_time_dto import SimTimeDto
from domain.dtos.translations_dto import TranslationsDto


@dataclass
class SeasonCompetitionDto:
    id: int
    date: SimTimeDto
    league_name: list[TranslationsDto]
    round: int
    event_type: EventTypeDto
