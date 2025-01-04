from domain.enums.activity_type import ActivityType
import random


def choose_free_activity() -> ActivityType:
    free_activities = [ActivityType.PRACTICE, ActivityType.LABOUR, ActivityType.IDLE]

    return random.choice(free_activities)
