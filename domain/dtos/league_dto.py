from dataclasses import dataclass


@dataclass
class LeagueDto:
    id: int
    name: str
    field_size: int
    level: int
