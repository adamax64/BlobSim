from pydantic import BaseModel

from domain.dtos.parent_dto import ParentDto


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
    is_rookie: bool = False
    at_risk: bool = False
    is_dead: bool = False
    is_retired: bool = False
    color: str
    parent: ParentDto | None = None
