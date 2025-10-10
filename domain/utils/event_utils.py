import random
from data.model.event_type import EventType


def pick_random_event_type() -> EventType:
    # Exclude non-competitive event types from random picks
    valid = [e for e in list(EventType) if e.name != 'CATCHUP_TRAINING']
    return random.choice(valid)
