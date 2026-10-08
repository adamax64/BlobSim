from pydantic import BaseModel, ConfigDict

from domain.dtos.blob_appearance_dto import BlobAppearanceDto


class GrandmasterStandingsDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    blob_id: int
    name: str
    appearance: BlobAppearanceDto
    championships: int
    gold: int
    silver: int
    bronze: int
    points: int
