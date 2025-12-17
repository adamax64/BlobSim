from dataclasses import dataclass

from data.model.policy_type import PolicyType
from domain.dtos.sim_time_dto import SimTimeDto


PolicyTypeDto = PolicyType


@dataclass
class PolicyDto():
    type: PolicyTypeDto
    effect_until: SimTimeDto
