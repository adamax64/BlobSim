from typing import List
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.event import Event
from data.model.league import League
from data.model.result import Result


@transactional
def get_results_of_league_by_season(league_id: int, season: int, session: Session) -> List[Result]:
    results = session.query(Result).join(Result.event).filter(Event.league_id == league_id, Event.season == season).all()
    return results


@transactional
def get_results_of_top_league_from_season(season: int, session: Session):
    results = session.query(Result).filter(Result.season >= season, Result.league_id == 1).all()
    return results


@transactional
def get_most_recent_real_league_result_of_blob(blob_id: int, session: Session) -> Result:
    result = (
        session.query(Result)
        .join(Result.event)
        .join(Event.league)
        .filter(Result.blob_id == blob_id, League.level != 0)
        .order_by(Event.date.desc())
        .first()
    )
    return result


@transactional
def save_all_results(session: Session, results: List[Result]) -> List[Result]:
    session.add_all(results)
    session.commit()
    for result in results:
        session.refresh(result)
    return results
