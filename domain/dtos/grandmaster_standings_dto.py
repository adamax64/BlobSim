from pydantic import BaseModel, ConfigDict


class GrandmasterStandingsDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blob_id: int
    name: str
    color: str
    championships: int
    gold: int
    silver: int
    bronze: int
    points: int
