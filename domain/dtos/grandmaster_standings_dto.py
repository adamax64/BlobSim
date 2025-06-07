from dataclasses import dataclass


@dataclass
class GrandmasterStandingsDTO:
    blob_id: int
    name: str
    color: str
    championships: int
    gold: int
    silver: int
    bronze: int
    points: int
