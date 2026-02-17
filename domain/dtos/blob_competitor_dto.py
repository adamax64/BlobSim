from dataclasses import dataclass

from domain.enums.state_type import StateTypeDto


@dataclass
class BlobCompetitorDto:
    id: int
    name: str
    strength: float
    speed: float
    color: str
    states: list[StateTypeDto]
