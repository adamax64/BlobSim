from typing import Dict, List
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.blob import Blob


@transactional
def get_all_living_blobs(session: Session) -> List[Blob]:
    result = session.query(Blob).filter(Blob.integrity > 0).all()
    return result


@transactional
def get_all_by_ids(session: Session, blob_ids) -> List[Blob]:
    result = session.query(Blob).filter(Blob.id.in_(blob_ids)).all()
    return result


@transactional
def get_all_by_league_order_by_id(session: Session, league_id: int) -> Dict[int, Blob]:
    result = session.query(Blob).filter(Blob.league_id == league_id).all()
    return {result.id: result for result in result}


@transactional
def get_blob_by_id(session: Session, blob_id: int) -> Blob:
    result = session.query(Blob).filter(Blob.id == blob_id).first()
    return result


@transactional
def save_all_blobs(session: Session, blobs: List[Blob]):
    session.add_all(blobs)
    session.commit()


@transactional
def save_blob(session: Session, blob: Blob):
    session.add(blob)
    session.commit()
