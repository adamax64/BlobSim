from typing import List
from sqlalchemy.orm import Session
import random

from data.db.db_engine import transactional
from data.model.event import Event
from data.persistence.blob_reposiotry import get_all_by_ids
from data.persistence.event_repository import get_event_by_date, get_previous_event_by_league_id_and_season, save_event
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_dto import EventDto
from domain.dtos.league_dto import LeagueDto
from domain.sim_data_service import get_current_calendar, get_sim_time
from domain.utils.sim_time_utils import get_season


@transactional
def get_or_start_event(session: Session, league_id: int, is_event_concluded: bool) -> EventDto:
    """ Get the current event or start a new one if there is none """

    current_calendar_event = get_current_calendar(session)
    if current_calendar_event is None:
        raise Exception("No event today according to calendar")
    time = get_sim_time(session)
    event = get_event_by_date(session, time)

    if event is None:
        season = get_season(time)
        previous_event = get_previous_event_by_league_id_and_season(session, league_id, season)
        current_round = 1 if previous_event is None else previous_event.round + 1
        event_type = current_calendar_event.event_type
        event = save_event(session, Event(league_id=league_id, date=time, season=season, round=current_round, type=event_type))

    actions = [ActionDto(
        blob_id=action.blob_id,
        tick=action.tick,
        score=action.score
    ) for action in event.actions]

    competitors = _get_competitors(session, event, is_event_concluded)
    random.shuffle(competitors)

    return EventDto(
        id=event.id,
        league=LeagueDto(id=event.league_id, name=event.league.name, field_size=len(competitors), level=event.league.level),
        actions=actions,
        competitors=competitors,
        season=event.season,
        round=event.round,
        type=event.type
    )


def _get_competitors(session: Session, event: Event, is_event_concluded: bool) -> List[BlobCompetitorDto]:
    if not is_event_concluded:
        return [BlobCompetitorDto(
            id=player.id,
            name=player.name,
            strength=player.strength
        ) for player in event.league.players]
    else:
        blob_ids = set([action.blob_id for action in event.actions])
        blobs = get_all_by_ids(session, blob_ids)
        return [BlobCompetitorDto(
            id=blob.id,
            name=blob.name,
            strength=blob.strength
        ) for blob in blobs]
