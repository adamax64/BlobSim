from pydantic import BaseModel

from domain.dtos.blob_appearance_dto import BlobAppearanceDto


class StandingsSnippetDto(BaseModel):
    blob_id: int
    blob_name: str
    appearance: BlobAppearanceDto
    position: int
    points: int
