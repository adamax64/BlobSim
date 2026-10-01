from pydantic import BaseModel, ConfigDict


class ActionDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blob_id: int
    scores: list[float]
