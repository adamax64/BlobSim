from dataclasses import dataclass, field

from domain.dtos.state_dto import StateDto
from domain.enums.element_dto import ElementDto


@dataclass
class BlobCompetitorDto:
    id: int
    name: str
    strength: float
    speed: float
    color: str
    states: list[StateDto]
    element: ElementDto = field(default=ElementDto.NONE)
