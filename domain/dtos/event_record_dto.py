from pydantic import BaseModel, ConfigDict

from domain.dtos.blob_dtos.blob_competitor_dto import BlobCompetitorDto


class ScoreDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    score: float | None = None
    best: bool = False
    personal_best: bool = False
    latest_score: float | None = None


class EventRecordDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blob: BlobCompetitorDto


class QuarteredEventRecordDto(EventRecordDto):
    quarters: list[ScoreDto]
    eliminated: bool = False
    current: bool = False
    next: bool = False


class RaceEventRecordDto(EventRecordDto):
    distance_records: list[float]
    previous_position: int = 1


class SprintEventRecordDto(RaceEventRecordDto):
    is_finished: bool = False
    time: float | None = None


class EliminationEventRecordDto(EventRecordDto):
    last_score: float | None = None
    eliminated: bool = False
    tick_wins: int = 0
