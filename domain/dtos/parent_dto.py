from pydantic import BaseModel

from domain.dtos.blob_appearance_dto import BlobAppearanceDto


class ParentDto(BaseModel):
    name: str
    appearance: BlobAppearanceDto
