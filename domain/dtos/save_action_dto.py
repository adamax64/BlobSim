from dataclasses import dataclass


@dataclass
class SaveActionDto():
    event_id: int
    tick: int
    blob_id: int
    score: float
