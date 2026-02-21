import enum
from pydantic import BaseModel

from domain.dtos.parent_dto import ParentDto
from domain.dtos.state_dto import StateDto
from domain.enums.activity_type import ActivityType


class IntegrityState(enum.Enum):
    POOR = "POOR"
    AVERAGE = "AVERAGE"
    GOOD = "GOOD"


class BlobStatsDto(BaseModel):
    name: str
    born: str
    terminated: str | None = None
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
    is_grandmaster: bool = False
    color: str
    parent: ParentDto | None = None
    money: int | None = None
    integrity_state: IntegrityState | None = None
    integrity_color: str | None = None
    current_activity: ActivityType | None = None
    current_standings_position: int | None = None
    states: list[StateDto]
