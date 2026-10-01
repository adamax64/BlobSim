from pydantic import BaseModel, ConfigDict

from domain.dtos.sim_time_dto import SimTimeDto
from domain.enums.state_type import StateTypeDto


class StateDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: StateTypeDto
    effect_until: SimTimeDto
