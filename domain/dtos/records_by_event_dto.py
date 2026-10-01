from pydantic import BaseModel, ConfigDict

from domain.dtos.blob_dtos.blob_stats_dto import BlobStatsDto
from domain.dtos.event_dto import EventTypeDto
from domain.dtos.league_dto import LeagueDto
from domain.dtos.record_dto import RecordDto


class WinsByEventDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_type: EventTypeDto
    blob: BlobStatsDto
    win_count: int


class RecordsByLeagueDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    league: LeagueDto
    records: list[RecordDto]


class RecordsByEventDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    winsByEvent: list[WinsByEventDto]
    recordsByLeague: list[RecordsByLeagueDto]
