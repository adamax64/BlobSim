from dataclasses import dataclass

from data.model.news_type import NewsTypeDbo
from domain.dtos.event_dto import EventTypeDto


NewsType = NewsTypeDbo


@dataclass
class TransfersDto():
    league_name: str
    blobs: list[str]


@dataclass
class NewsDto():
    date: int
    type: NewsType
    blob_name: str | None = None
    league_name: str | None = None
    round: int | None = None
    season: int | None = None
    event_type: EventTypeDto | None = None
    winner: str | None = None
    second: str | None = None
    third: str | None = None
    transfers: list[TransfersDto] | None = None
    retired: list[str] | None = None
    rookies: list[str] | None = None
    grandmaster: str | None = None
