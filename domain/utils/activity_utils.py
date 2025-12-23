from domain.enums.activity_type import ActivityType
import random

FREE_ACTIVITIES = [ActivityType.PRACTICE, ActivityType.LABOUR, ActivityType.IDLE, ActivityType.MINING]


def choose_activity(extra_activities: list[ActivityType]) -> ActivityType:
    activities = FREE_ACTIVITIES + extra_activities

    return random.choice(activities)
