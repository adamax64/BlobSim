from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.blob import Blob


@transactional
def get_all_blobs_by_name(
    session: Session, name_search: str = None, show_dead: bool = False
) -> list[Blob]:
    result = (
        session.query(Blob)
        .filter(
            and_(
                name_search is None or or_(Blob.first_name.contains(name_search), Blob.last_name.contains(name_search)),
                or_(show_dead, Blob.integrity > 0),
            )
        )
        .all()
    )
    return result


@transactional
def get_all_by_ids(session: Session, blob_ids) -> list[Blob]:
    result = session.query(Blob).filter(Blob.id.in_(blob_ids)).all()
    return result


@transactional
def get_all_retired(session: Session) -> list[Blob]:
    result = session.query(Blob).filter(and_(Blob.terminated.is_(None), Blob.league_id.is_(None))).all()
    return result


@transactional
def get_all_by_league_order_by_id(session: Session, league_id: int) -> dict[int, Blob]:
    results = session.query(Blob).filter(Blob.league_id == league_id).all()
    return {result.id: result for result in results}


@transactional
def get_blob_by_id(session: Session, blob_id: int) -> Blob:
    result = session.query(Blob).filter(Blob.id == blob_id).first()
    return result


@transactional
def save_all_blobs(session: Session, blobs: list[Blob]):
    session.add_all(blobs)
    session.commit()


@transactional
def save_blob(session: Session, blob: Blob) -> Blob:
    session.add(blob)
    session.commit()
    session.refresh(blob)
    return blob


@transactional
def get_youngest_blob_debuting_in_season(session: Session, season: int) -> Blob | None:
    """Return the youngest blob (largest born timestamp) whose debut equals the given season."""
    return (
        session.query(Blob)
        .filter(Blob.debut == season)
        .order_by(Blob.born.desc())
        .first()
    )
