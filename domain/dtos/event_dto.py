from pydantic import BaseModel, ConfigDict

from data.model.event_type import EventType
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.league_dto import LeagueDto


EventTypeDto = EventType


class EventDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competitors: list[BlobCompetitorDto]
    actions: list[ActionDto]
    league: LeagueDto
    season: int
    round: int
    type: EventTypeDto
    isFinished: bool
