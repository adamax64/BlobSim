from pydantic import BaseModel


class BlobStatsDto(BaseModel):
    name: str
    born: str
    debut: int | None = None
    contract: int | None = None
    podiums: int
    wins: int
    championships: int
    grandmasters: int
    league_name: str
    at_risk: bool = False
    is_dead: bool = False
    is_retired: bool = False
