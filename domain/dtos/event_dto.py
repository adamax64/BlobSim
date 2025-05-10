from dataclasses import dataclass
from typing import List

from data.model.event_type import EventType
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_record_dto import QuarteredEventRecordDto, RaceEventRecordDto
from domain.dtos.league_dto import LeagueDto


EventTypeDto = EventType


@dataclass
class EventDto:
    id: int
    competitors: List[BlobCompetitorDto]
    actions: List[ActionDto]
    event_records: List[QuarteredEventRecordDto | RaceEventRecordDto]
    league: LeagueDto
    season: int
    round: int
    type: EventTypeDto
