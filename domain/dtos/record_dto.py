from data.model.event_type import EventType
from pydantic import BaseModel


class RecordDto(BaseModel):
    id: int
    league_id: int
    event_type: EventType
    competitor_id: int
    score: float
