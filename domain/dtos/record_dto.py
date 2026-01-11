from data.model.event_type import EventType
from pydantic import BaseModel

from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.dtos.league_dto import LeagueDto


class RecordDto(BaseModel):
    id: int
    league: LeagueDto
    event_type: EventType
    blob: BlobStatsDto
    score: float
