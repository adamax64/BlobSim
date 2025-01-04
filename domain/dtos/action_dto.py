from dataclasses import dataclass


@dataclass
class ActionDto():
    tick: int
    blob_id: int
    score: float
