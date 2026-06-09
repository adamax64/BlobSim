import random
from data.model.event_type import EventType

EXCLUDED_EVENT_TYPES: frozenset[EventType] = frozenset(
    {
        EventType.CATCHUP_TRAINING,
        EventType.QUARTERED_ONE_SHOT_SCORING,
        EventType.QUARTERED_TWO_SHOT_SCORING,
    }
)


def get_allowed_event_types() -> list[EventType]:
    return [event_type for event_type in EventType if event_type not in EXCLUDED_EVENT_TYPES]


def build_random_event_type_sequence(count: int) -> list[EventType]:
    allowed = get_allowed_event_types()
    if count <= 0:
        return []
    if count >= len(allowed):
        sequence = list(allowed)
        sequence.extend(random.choice(allowed) for _ in range(count - len(allowed)))
        random.shuffle(sequence)
        return sequence
    return random.sample(allowed, count)
