from dataclasses import dataclass


@dataclass
class BlobStatsDto:
    name: str
    born: int
    debut: int
    contract: int
    podiums: int
    wins: int
    championships: int
    grandmasters: int
    league_name: str
