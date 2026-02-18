from dataclasses import dataclass

from domain.enums.state_type import StateTypeDto


@dataclass
class StateDto:
    type: StateTypeDto
    effect_until: int
