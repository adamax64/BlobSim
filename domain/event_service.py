from typing import List
from sqlalchemy.orm import Session
import random

from data.db.db_engine import transactional
from data.model.event import Event
from data.persistence.blob_reposiotry import get_all_by_ids
from data.persistence.event_repository import (
    get_event_by_date,
    get_event_by_id as repository_get_event_by_id,
    get_previous_event_by_league_id_and_season,
    save_event
)
from data.persistence.result_repository import get_results_of_event
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_dto import EventDto
from domain.dtos.event_summary_dto import EventSummaryDTO
from domain.dtos.league_dto import LeagueDto
from domain.exceptions.event_not_found_exception import EventNotFoundException
from domain.exceptions.no_current_event_exception import NoCurrentEventException
from domain.sim_data_service import get_current_calendar, get_sim_time
from domain.utils.blob_name_utils import format_blob_name
from domain.utils.sim_time_utils import get_season


@transactional
def get_or_start_event(session: Session, league_id: int, is_event_concluded: bool) -> EventDto:
    """ Get the current event or start a new one if there is none """

    current_calendar_event = get_current_calendar(session)
    if current_calendar_event is None:
        raise NoCurrentEventException()
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


@transactional
def get_event_by_id(event_id: int, session: Session, check_date: bool = False) -> EventDto:
    """ Get event by id """
    event = repository_get_event_by_id(session, event_id)
    if event is None:
        raise EventNotFoundException()
    if check_date and event.date < get_sim_time(session):
        raise NoCurrentEventException()

    actions = [ActionDto(
        blob_id=action.blob_id,
        tick=action.tick,
        score=action.score
    ) for action in event.actions]

    competitors = _get_competitors(session, event, False)
    return EventDto(
        id=event.id,
        league=LeagueDto(id=event.league_id, name=event.league.name, field_size=len(competitors), level=event.league.level),
        actions=actions,
        competitors=competitors,
        season=event.season,
        round=event.round,
        type=event.type
    )


@transactional
def get_concluded_event_summary(session: Session) -> str | None:
    """ Get the summary of the last concluded event """
    current_calendar_event = get_current_calendar(session)
    if current_calendar_event is None or not current_calendar_event.concluded:
        return None
    event = get_event_by_date(session, current_calendar_event.date)
    results = get_results_of_event(event.id, session)

    return EventSummaryDTO(
        event_name=f"{event.league.name}, S{event.season} R{event.round}",
        winner=format_blob_name(results[0].blob),
        runner_up=format_blob_name(results[1].blob),
        third_place=format_blob_name(results[2].blob)
    )


def _get_competitors(session: Session, event: Event, is_event_concluded: bool) -> List[BlobCompetitorDto]:
    if not is_event_concluded:
        return [BlobCompetitorDto(
            id=player.id,
            name=format_blob_name(player),
            strength=player.strength,
            color=player.color
        ) for player in event.league.players]
    else:
        blob_ids = set([action.blob_id for action in event.actions])
        blobs = get_all_by_ids(session, blob_ids)
        return [BlobCompetitorDto(
            id=blob.id,
            name=format_blob_name(blob),
            strength=blob.strength,
            color=blob.color
        ) for blob in blobs]
