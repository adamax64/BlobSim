from dataclasses import dataclass

from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.dtos.event_dto import EventTypeDto
from domain.dtos.league_dto import LeagueDto
from domain.dtos.record_dto import RecordDto


@dataclass
class WinsByEventDto:
    event_type: EventTypeDto
    blob: BlobStatsDto
    win_count: int


@dataclass
class RecordsByEventDto:
    winsByEvent: list[WinsByEventDto]
    recordsByEvent: dict[LeagueDto, list[RecordDto]]
