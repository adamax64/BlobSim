from pydantic import BaseModel, ConfigDict

from domain.dtos.event_dto import EventTypeDto
from domain.dtos.sim_time_dto import SimTimeDto
from domain.dtos.translations_dto import TranslationsDto


class SeasonCompetitionDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: SimTimeDto
    league_name: list[TranslationsDto]
    round: int
    event_type: EventTypeDto
