from domain.enums.activity_type import ActivityType
import random

FREE_ACTIVITIES = [
    ActivityType.PRACTICE,
    ActivityType.LABOUR,
    ActivityType.IDLE,
    ActivityType.MINING,
    ActivityType.INTENSE_PRACTICE,
]


def choose_activity(extra_activities: list[ActivityType]) -> ActivityType:
    activities = FREE_ACTIVITIES + extra_activities

    weights = [10, 10, 10, 10, 1] + [10] * len(extra_activities)

    return random.choices(activities, weights=weights)[0]
