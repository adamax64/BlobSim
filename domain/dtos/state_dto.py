from dataclasses import dataclass

from domain.dtos.sim_time_dto import SimTimeDto
from domain.enums.state_type import StateTypeDto


@dataclass
class StateDto:
    type: StateTypeDto
    effect_until: SimTimeDto
