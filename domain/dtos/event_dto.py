from dataclasses import dataclass
from typing import List

from data.model.event_type import EventType
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.league_dto import LeagueDto


EventTypeDto = EventType


@dataclass
class EventDto:
    id: int
    competitors: List[BlobCompetitorDto]
    actions: List[ActionDto]
    league: LeagueDto
    season: int
    round: int
    type: EventTypeDto
