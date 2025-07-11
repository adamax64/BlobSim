from dataclasses import dataclass

from domain.dtos.blob_competitor_dto import BlobCompetitorDto


@dataclass
class ScoreDto():
    score: float | None = None
    best: bool = False
    personal_best: bool = False
    latest_score: float | None = None


@dataclass
class EventRecordDto():
    blob: BlobCompetitorDto


@dataclass
class QuarteredEventRecordDto(EventRecordDto):
    quarters: list[ScoreDto]
    eliminated: bool = False
    current: bool = False
    next: bool = False


@dataclass
class RaceEventRecordDto(EventRecordDto):
    distance_records: list[float]
    previous_position: int = 1
