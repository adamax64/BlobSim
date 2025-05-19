from dataclasses import dataclass


@dataclass
class SimTimeDto:
    eon: int
    season: int
    epoch: int
    cycle: int
