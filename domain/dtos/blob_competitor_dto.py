from dataclasses import dataclass


@dataclass
class BlobCompetitorDto():
    id: int
    name: str
    strength: float
    color: str
