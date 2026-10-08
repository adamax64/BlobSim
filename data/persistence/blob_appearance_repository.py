from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.blob_appearance import BlobAppearance


@transactional
def save_blob_appearance(
    session: Session, blob_appearance: BlobAppearance
) -> BlobAppearance:
    session.add(blob_appearance)
    session.commit()
    session.refresh(blob_appearance)
    return blob_appearance
