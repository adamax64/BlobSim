from dataclasses import dataclass

from domain.dtos.state_dto import StateDto


@dataclass
class BlobCompetitorDto:
    id: int
    name: str
    strength: float
    speed: float
    color: str
    states: list[StateDto]
