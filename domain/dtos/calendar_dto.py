from dataclasses import dataclass


@dataclass
class CalendarDto:
    date: int
    league_name: str
    is_concluded: bool
