
from dataclasses import dataclass


@dataclass
class EventSummaryDTO:
    """
    Data Transfer Object for Event Summary.
    """
    event_name: str
    winner: str
    runner_up: str
    third_place: str
