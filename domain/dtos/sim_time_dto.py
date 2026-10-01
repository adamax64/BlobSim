from pydantic import BaseModel, ConfigDict


class SimTimeDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    eon: int
    season: int
    epoch: int
    cycle: int
