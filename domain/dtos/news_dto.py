from dataclasses import dataclass

from data.model.news_type import NewsType
from domain.dtos.event_dto import EventTypeDto
from domain.dtos.sim_time_dto import SimTimeDto
from domain.dtos.blob_stats_dto import BlobStatsDto


NewsTypeDto = NewsType


@dataclass
class TransfersDto():
    league_name: str
    blobs: list[BlobStatsDto]


@dataclass
class NewsDto():
    date: SimTimeDto
    type: NewsTypeDto
    blob: BlobStatsDto | None = None
    league_name: str | None = None
    round: int | None = None
    season: int | None = None
    event_type: EventTypeDto | None = None
    winner: BlobStatsDto | None = None
    second: BlobStatsDto | None = None
    third: BlobStatsDto | None = None
    transfers: list[TransfersDto] | None = None
    retired: list[BlobStatsDto] | None = None
    rookies: list[BlobStatsDto] | None = None
    grandmaster: BlobStatsDto | None = None
