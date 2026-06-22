import random
from sqlalchemy.orm import Session
from data.db.db_engine import transactional
from data.model.item_type import ItemType
from data.model.state_type import StateType
from data.persistence.blob_reposiotry import get_blob_by_id
from data.persistence.item_repository import delete_item
from data.persistence.state_repository import create_state
from domain.sim_data_service import get_sim_time
from domain.utils.constants import INITIAL_INTEGRITY
from domain.utils.item_utils import get_item_from_list_by_type


INJURED_STATE_DURATION = 4


@transactional
def apply_injury(blob_id: int, session: Session):
    blob = get_blob_by_id(session, blob_id)

    repair_kit = get_item_from_list_by_type(blob.items, ItemType.REPAIR_KIT)
    if repair_kit:
        delete_item(repair_kit)
        return

    effect_until = get_sim_time(session) + INJURED_STATE_DURATION
    if random.random() < max(0, (1 - blob.integrity / INITIAL_INTEGRITY) * 0.2):
        blob.integrity -= 1
    create_state(session, blob.id, StateType.INJURED, effect_until)
