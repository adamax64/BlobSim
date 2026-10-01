from pydantic import BaseModel, ConfigDict

from domain.dtos.state_dto import StateDto
from domain.enums.element_dto import ElementDto


class BlobCompetitorDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    strength: float
    speed: float
    color: str
    states: list[StateDto]
    element: ElementDto = ElementDto.NONE
