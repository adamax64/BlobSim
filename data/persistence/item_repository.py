from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.item import Item


@transactional
def get_items_of_blob(session: Session, blob_id: int) -> list[Item]:
    return session.query(Item).filter(Item.blob_id == blob_id).all()


@transactional
def save_item(session: Session, item: Item) -> Item:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@transactional
def delete_item(session: Session, item_id: int):
    session.query(Item).filter(Item.id == item_id).delete()
    session.commit()


@transactional
def update_item(session: Session, item: Item) -> Item:
    session.commit()
    session.refresh(item)
    return item
