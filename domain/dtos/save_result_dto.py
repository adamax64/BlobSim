from dataclasses import dataclass


@dataclass
class SaveResultDto():
    event_id: int
    blob_id: int
    position: int
    points: int
