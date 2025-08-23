from dataclasses import dataclass


@dataclass
class ActionDto():
    blob_id: int
    scores: list[float]
