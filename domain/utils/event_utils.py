import random
from data.model.event_type import EventType


def pick_random_event_type() -> EventType:
    return random.choice(list(EventType))
