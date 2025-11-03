import enum
from pydantic import BaseModel

from domain.dtos.parent_dto import ParentDto
from domain.enums.activity_type import ActivityType


class SpeedCategory(enum.Enum):
    SLOW = "SLOW"
    AVERAGE = "AVERAGE"
    FAST = "FAST"


class StrengthCategory(enum.Enum):
    WEAK = "WEAK"
    AVERAGE = "AVERAGE"
    STRONG = "STRONG"


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
    speed_category: SpeedCategory | None = None
    strength_category: StrengthCategory | None = None
    integrity_state: IntegrityState | None = None
    speed_color: str | None = None
    strength_color: str | None = None
    integrity_color: str | None = None
    current_activity: ActivityType | None = None
