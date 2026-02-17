from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.state import State
from data.model.state_type import StateType


@transactional
def get_states_of_blob(session: Session, blob_id: int) -> list[State]:
    return session.query(State).filter(State.blob_id == blob_id).all()


@transactional
def save_state(session: Session, state: State) -> State:
    session.add(state)
    session.commit()
    session.refresh(state)
    return state


@transactional
def create_state(
    session: Session, blob_id: int, state_type: StateType, effect_until: int
) -> State:
    state = State(blob_id=blob_id, type=state_type, effect_until=effect_until)
    session.add(state)
    session.commit()
    session.refresh(state)
    return state
