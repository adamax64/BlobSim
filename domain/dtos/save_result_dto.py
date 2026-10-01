from pydantic import BaseModel, ConfigDict


class SaveResultDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_id: int
    blob_id: int
    position: int
    points: int
