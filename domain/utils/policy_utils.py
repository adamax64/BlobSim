import random
from data.model.policy_type import PolicyType


def choose_random_policy_type() -> PolicyType:
    policy_types = [
        PolicyType.FACTORY_MODERNIZATION,
        PolicyType.PENSION_SCHEME,
        PolicyType.LABOUR_SUBSIDIES,
        PolicyType.GYM_IMPROVEMENT
    ]
    return random.choice(policy_types)


def get_policy_effect_duration(level: int) -> int:
    if level <= 1:
        return 4
    elif level == 2:
        return 6
    else:
        return 6 + (level - 2)
