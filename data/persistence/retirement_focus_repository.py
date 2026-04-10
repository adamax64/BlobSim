from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.retirement_focus import RetirementFocus
from data.model.retirement_focus_type import RetirementFocusType


@transactional
def set_retirement_focus(
    session: Session, blob_id: int, focus_type: RetirementFocusType
):
    """Set the retirement focus for a blob."""

    session.add(RetirementFocus(blob_id=blob_id, focus_type=focus_type))


@transactional
def remove_retirement_focus(session: Session, blob_id: int):
    """Remove the retirement focus for a blob."""

    focus = session.query(RetirementFocus).filter_by(blob_id=blob_id).first()
    if focus:
        session.delete(focus)
