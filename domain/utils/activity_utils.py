from data.model.blob import Blob
from data.model.state_type import StateType
from domain.enums.activity_type import ActivityType
import random

from domain.utils.blob_utils import has_state, has_trait
from data.model.trait_type import TraitType


FREE_ACTIVITIES = [
    ActivityType.PRACTICE,
    ActivityType.LABOUR,
    ActivityType.IDLE,
    ActivityType.MINING,
    ActivityType.INTENSE_PRACTICE,
]

idx_practice = 0
idx_labour = 1
idx_idle = 2
idx_intense_practice = 4


def choose_activity(
    blob: Blob, extra_activities: list[ActivityType] = []
) -> ActivityType:
    """Choose an activity for `blob` with weights adjusted by traits.

    `session` is passed to query traits via the persistence layer.
    """
    activities = FREE_ACTIVITIES + extra_activities

    # base weights corresponding to FREE_ACTIVITIES
    base = [10, 10, 10, 10, 1]

    # start with base weights
    weights = base.copy()

    # ensure weights list extends for extra activities
    for activity in extra_activities:
        if activity == ActivityType.ADMINISTRATION:
            weight = 10
            if has_trait(blob, TraitType.DETERMINED):
                weight *= 2
            if has_trait(blob, TraitType.LAZY):
                weight = weight / 2 + 1
            if has_state(blob, StateType.TIRED) or has_state(blob, StateType.GLOOMY):
                weight /= 2
            weights.append(weight)
        else:
            weights.append(10)

    # adjust weights based on traits and states
    hard_working = has_trait(blob, TraitType.HARD_WORKING)
    determined = has_trait(blob, TraitType.DETERMINED)
    lazy = has_trait(blob, TraitType.LAZY)

    injured = has_state(blob, StateType.INJURED)
    tired = has_state(blob, StateType.TIRED)
    gloomy = has_state(blob, StateType.GLOOMY)

    if hard_working:
        weights[idx_labour] *= 2

    if determined:
        weights[idx_practice] *= 2
        weights[idx_intense_practice] *= 10

    if lazy:
        weights[idx_labour] /= 2
        weights[idx_practice] /= 2
        weights[idx_intense_practice] = 0

    if injured:
        weights[idx_labour] = 0
        weights[idx_practice] /= 2
        weights[idx_intense_practice] = 0

    if tired:
        weights[idx_practice] /= 2
        weights[idx_intense_practice] = 0

    if gloomy:
        weights[idx_idle] *= 2

    return random.choices(activities, weights=weights, k=1)[0]
