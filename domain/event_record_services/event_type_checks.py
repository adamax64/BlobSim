from domain.dtos.event_dto import EventTypeDto


def is_quartered_event(event_type: EventTypeDto) -> bool:
    return event_type in [
        EventTypeDto.QUARTERED_ONE_SHOT_SCORING,
        EventTypeDto.QUARTERED_ONE_SHOT_SCORING_V2,
        EventTypeDto.QUARTERED_TWO_SHOT_SCORING,
        EventTypeDto.QUARTERED_TWO_SHOT_SCORING_V2,
    ]


def is_quartered_two_shot_event(event_type: EventTypeDto) -> bool:
    return event_type in [
        EventTypeDto.QUARTERED_TWO_SHOT_SCORING,
        EventTypeDto.QUARTERED_TWO_SHOT_SCORING_V2,
    ]


def is_quartered_event_v1(event_type: EventTypeDto) -> bool:
    return event_type in [
        EventTypeDto.QUARTERED_ONE_SHOT_SCORING,
        EventTypeDto.QUARTERED_TWO_SHOT_SCORING,
    ]
