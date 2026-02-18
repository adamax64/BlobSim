from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.trait import Trait


@transactional
def get_traits_of_blob(session: Session, blob_id: int) -> list[Trait]:
    return session.query(Trait).filter(Trait.blob_id == blob_id).all()


@transactional
def save_trait(session: Session, trait: Trait) -> Trait:
    session.add(trait)
    session.commit()
    session.refresh(trait)
    return trait


@transactional
def delete_trait(session: Session, trait_id: int):
    session.query(Trait).filter(Trait.id == trait_id).delete()
    session.commit()
