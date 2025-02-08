from dataclasses import dataclass
from typing import List

from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from dataclasses import field


@dataclass
class ScoreDto():
    score: float | None = None
    scoring_progress: int | None = None
    best: bool = False
    personal_best: bool = False
    latest_score: int | None = None


@dataclass
class EventRecordDto():
    blob: BlobCompetitorDto


@dataclass
class QuarteredEventRecordDto(EventRecordDto):
    quarters: List[ScoreDto]


@dataclass
class RaceEventRecordDto(EventRecordDto):
    distance_records: List[float] = field(default_factory=list)
    time_records: List[float] = field(default_factory=list)
    previous_position: int = 1
