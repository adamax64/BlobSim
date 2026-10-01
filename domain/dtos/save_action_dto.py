from pydantic import BaseModel, ConfigDict


class SaveActionDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_id: int
    tick: int
    blob_id: int
    score: float
