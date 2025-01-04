from dataclasses import dataclass
from typing import List

from domain.dtos.blob_competitor_dto import BlobCompetitorDto


@dataclass
class ScoreDto():
    score: float | None = None
    scoring_progress: int | None = None
    best: bool = False
    personal_best: bool = False
    latest_score: int | None = None


@dataclass
class QuarteredEventRecordDto():
    blob: BlobCompetitorDto
    quarters: List[ScoreDto]
