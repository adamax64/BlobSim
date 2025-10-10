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
def get_blob_relative_strengths_by_blob(session: Session) -> dict[int, float]:
    """
    Get the relative strength of each blob compared to all other living blobs in the database.
    The relative strength is a value between 0 and 1, where 0 is the weakest blob and 1 is the strongest blob.
    """
    blobs = session.query(Blob).where(Blob.integrity > 0).all()
    if not blobs:
        return {}

    max_strength = max(blob.strength for blob in blobs)
    min_strength = min(blob.strength for blob in blobs)

    if max_strength == min_strength:
        return {blob.id: 0.0 for blob in blobs}

    return {
        blob.id: (blob.strength - min_strength) / (max_strength - min_strength)
        for blob in blobs
    }


@transactional
def get_blob_relative_speeds_by_blob(session: Session) -> dict[int, float]:
    """
    Get the relative speeds of each blob compared to all other living blobs in the database.
    The relative speed is a value between 0 and 1, where 0 is the slowest blob and 1 is the fastest blob.
    """
    blobs = session.query(Blob).where(Blob.integrity > 0).all()
    if not blobs:
        return {}

    max_speed = max(blob.speed for blob in blobs)
    min_speed = min(blob.speed for blob in blobs)

    if max_speed == min_speed:
        return {blob.id: 0.0 for blob in blobs}

    return {
        blob.id: (blob.speed - min_speed) / (max_speed - min_speed)
        for blob in blobs
    }


@transactional
def get_youngest_blob_debuting_in_season(session: Session, season: int) -> Blob | None:
    """Return the youngest blob (largest born timestamp) whose debut equals the given season."""
    return (
        session.query(Blob)
        .filter(Blob.debut == season)
        .order_by(Blob.born.desc())
        .first()
    )
