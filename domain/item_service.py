import random

from sqlalchemy.orm import Session

from data.model.blob import Blob
from data.model.item import Item
from data.model.item_type import ItemType
from data.model.state_type import StateType
from data.persistence.item_repository import (
    delete_item,
    get_items_of_blob,
    save_item,
    update_item,
)
from data.persistence.state_repository import create_state, delete_state
from domain.sim_data_service import get_sim_time
from domain.utils.item_utils import (
    INFINITE_DURABILITY,
    PRE_EVENT_ITEM_STATE_TYPES,
    PRE_EVENT_ITEM_TYPES,
    get_inventory_capacity,
    get_item_durability,
    get_item_rarity_rank,
    get_item_sell_value,
    is_consumable,
)

OVERCLOCK_DEPLETED_INJURY_CHANCE = 0.3
INJURED_STATE_DURATION = 4
EVENT_ITEM_STATE_DURATION = 1

MONEY_REWARDS: dict[ItemType, int] = {
    ItemType.COIN: 1,
    ItemType.BAG_OF_MONEY: 5,
    ItemType.TREASURE_CHEST: 20,
}

ENERGY_CELL_TARGET_TYPES = {ItemType.POWER_BANK, ItemType.OVERCLOCKING_DEVICE}


def grant_item_to_blob(blob: Blob, item_type: ItemType, session: Session) -> None:
    if item_type in MONEY_REWARDS:
        blob.money += MONEY_REWARDS[item_type]
        return

    if item_type == ItemType.MAINTENANCE_KIT:
        blob.integrity += 3
        return

    if item_type == ItemType.ENERGY_CELL and _consume_energy_cell(blob, session):
        return

    if item_type == ItemType.REPAIR_KIT and _consume_repair_kit(blob, session):
        return

    _add_item_to_inventory(blob, item_type, session)


def is_inventory_full(blob: Blob, session: Session) -> bool:
    items = get_items_of_blob(session, blob.id)
    return len(items) >= get_inventory_capacity(items)


def apply_pre_event_items(blob_id: int, session: Session) -> None:
    effect_until = get_sim_time(session) + EVENT_ITEM_STATE_DURATION

    for item in list(get_items_of_blob(session, blob_id)):
        if item.type not in PRE_EVENT_ITEM_TYPES or not _can_use_pre_event_item(item):
            continue

        if (
            item.type == ItemType.OVERCLOCKING_DEVICE
            and item.durability == 0
            and random.random() < OVERCLOCK_DEPLETED_INJURY_CHANCE
        ):
            create_state(
                session,
                blob_id,
                StateType.INJURED,
                get_sim_time(session) + INJURED_STATE_DURATION,
            )

        create_state(
            session,
            blob_id,
            PRE_EVENT_ITEM_STATE_TYPES[item.type],
            effect_until,
        )
        _consume_item_after_use(session, item)


def _can_use_pre_event_item(item: Item) -> bool:
    if is_consumable(item.type):
        return True 
    if item.type == ItemType.OVERCLOCKING_DEVICE:
        # If Durability is 0 blobs don't always use because it is dangerous
        return item.durability > 0 or random.random() < OVERCLOCK_DEPLETED_INJURY_CHANCE
    return item.durability > 0


def _consume_item_after_use(session: Session, item: Item) -> None:
    # TODO: use cache cleaner or energy cell if reasonable
    if is_consumable(item.type):
        delete_item(session, item.id)
        return
    if item.durability == INFINITE_DURABILITY:
        return
    if item.durability > 0:
        item.durability -= 1
    
    update_item(session, item)


def _add_item_to_inventory(blob: Blob, item_type: ItemType, session: Session) -> None:
    items = get_items_of_blob(session, blob.id)
    if len(items) < get_inventory_capacity(items):
        save_item(
            session,
            Item(
                blob_id=blob.id,
                type=item_type,
                durability=get_item_durability(item_type),
            ),
        )
        return

    new_rank = get_item_rarity_rank(item_type)
    depleted_unconsumables = [
        item
        for item in items
        if not is_consumable(item.type) and item.durability == 0
    ]
    if depleted_unconsumables:
        to_sell = min(
            depleted_unconsumables, key=lambda item: get_item_rarity_rank(item.type)
        )
        _sell_item(blob, to_sell, session)
        save_item(
            session,
            Item(
                blob_id=blob.id,
                type=item_type,
                durability=get_item_durability(item_type),
            ),
        )
        return

    lower_rarity_items = [
        item for item in items if get_item_rarity_rank(item.type) < new_rank
    ]
    if lower_rarity_items:
        to_sell = min(
            lower_rarity_items, key=lambda item: get_item_rarity_rank(item.type)
        )
        _sell_item(blob, to_sell, session)
        save_item(
            session,
            Item(
                blob_id=blob.id,
                type=item_type,
                durability=get_item_durability(item_type),
            ),
        )
        return

    blob.money += get_item_sell_value(item_type)


def _sell_item(blob: Blob, item: Item, session: Session) -> None:
    blob.money += get_item_sell_value(item.type)
    delete_item(session, item.id)


def _consume_energy_cell(blob: Blob, session: Session) -> bool:
    rechargeable_items = [
        item
        for item in get_items_of_blob(session, blob.id)
        if item.type in ENERGY_CELL_TARGET_TYPES
    ]
    if not rechargeable_items:
        return False

    item = random.choice(rechargeable_items)
    item.durability = get_item_durability(item.type)
    update_item(session, item)
    return True


def _consume_repair_kit(blob: Blob, session: Session) -> bool:
    current_time = get_sim_time(session)
    for state in blob.states:
        if state.type == StateType.INJURED and state.effect_until >= current_time:
            delete_state(session, state.id)
            session.refresh(blob)
            return True
    return False
