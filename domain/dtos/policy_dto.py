from pydantic import BaseModel, ConfigDict

from data.model.policy_type import PolicyType
from domain.dtos.sim_time_dto import SimTimeDto


PolicyTypeDto = PolicyType


class PolicyDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: PolicyTypeDto
    effect_until: SimTimeDto
