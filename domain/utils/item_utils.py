import random

from data.model.item_type import ItemType
from data.model.state_type import StateType

DEFAULT_UNCONSUMABLE_DURABILITY = 3
INFINITE_DURABILITY = -1
DEFAULT_INVENTORY_SIZE = 3
EXTERNAL_STORAGE_INVENTORY_BONUS = 3

RARITY_RANK = {"common": 0, "rare": 1, "epic": 2, "legendary": 3}

MONEY_ITEM_VALUES_BY_RARITY = {
    "common": 1,
    "rare": 5,
    "epic": 10,
    "legendary": 20,
}

CONSUMABLE_ITEMS = {
    ItemType.COOKIE,
    ItemType.COIN,
    ItemType.ENERGY_CELL,
    ItemType.BAG_OF_MONEY,
    ItemType.CACHE_CLEANER,
    ItemType.MAINTENANCE_KIT,
    ItemType.SACK_OF_MONEY,
    ItemType.REPAIR_KIT,
    ItemType.TREASURE_CHEST,
}

UNCONSUMABLE_DURABILITY_OVERRIDES: dict[ItemType, int] = {
    ItemType.PROCESSOR_PASTE: 16,
    ItemType.EXTERNAL_STORAGE: INFINITE_DURABILITY,
}

ITEM_RARITY_TIERS: dict[str, tuple[ItemType, ...]] = {
    "common": (ItemType.COOKIE, ItemType.COIN),
    "rare": (
        ItemType.ENERGY_CELL,
        ItemType.BAG_OF_MONEY,
        ItemType.CACHE_CLEANER,
        ItemType.CACHE,
    ),
    "epic": (
        ItemType.MAINTENANCE_KIT,
        ItemType.SACK_OF_MONEY,
        ItemType.REPAIR_KIT,
        ItemType.POWER_BANK,
        ItemType.PROCESSOR_PASTE,
    ),
    "legendary": (
        ItemType.TREASURE_CHEST,
        ItemType.OVERCLOCKING_DEVICE,
        ItemType.EXTERNAL_STORAGE,
    ),
}

RARITY_WEIGHTS = [60, 20, 16, 4]

PRE_EVENT_ITEM_TYPES = {
    ItemType.COOKIE,
    ItemType.ENERGY_CELL,
    ItemType.CACHE,
    ItemType.POWER_BANK,
    ItemType.OVERCLOCKING_DEVICE,
}

PRE_EVENT_ITEM_STATE_TYPES: dict[ItemType, StateType] = {
    ItemType.COOKIE: StateType.COOKIE_BOOST,
    ItemType.ENERGY_CELL: StateType.ENERGY_CELL_BOOST,
    ItemType.CACHE: StateType.CACHE_BOOST,
    ItemType.POWER_BANK: StateType.POWER_BANK_BOOST,
    ItemType.OVERCLOCKING_DEVICE: StateType.OVERCLOCKING_DEVICE_BOOST,
}

PRE_EVENT_SKILL_STATE_BONUSES: dict[StateType, float] = {
    StateType.COOKIE_BOOST: 0.04,
    StateType.POWER_BANK_BOOST: 0.02,
    StateType.OVERCLOCKING_DEVICE_BOOST: 0.10,
}

PRE_EVENT_MIN_SCORE_STATE_BONUSES: dict[StateType, float] = {
    StateType.ENERGY_CELL_BOOST: 0.05,
    StateType.CACHE_BOOST: 0.05,
    StateType.POWER_BANK_BOOST: 0.10,
}


def get_item_rarity(item_type: ItemType) -> str:
    for tier, types in ITEM_RARITY_TIERS.items():
        if item_type in types:
            return tier
    raise ValueError(f"Unknown item type: {item_type}")


def get_item_rarity_rank(item_type: ItemType) -> int:
    return RARITY_RANK[get_item_rarity(item_type)]


def get_item_sell_value(item_type: ItemType) -> int:
    return MONEY_ITEM_VALUES_BY_RARITY[get_item_rarity(item_type)]


def is_consumable(item_type: ItemType) -> bool:
    return item_type in CONSUMABLE_ITEMS


def get_inventory_capacity(items: list) -> int:
    external_storage_count = sum(
        1 for item in items if item.type == ItemType.EXTERNAL_STORAGE
    )
    return DEFAULT_INVENTORY_SIZE + EXTERNAL_STORAGE_INVENTORY_BONUS * external_storage_count


def choose_random_item_type() -> ItemType:
    tier = random.choices(
        list(ITEM_RARITY_TIERS.keys()), weights=RARITY_WEIGHTS, k=1
    )[0]
    return random.choice(ITEM_RARITY_TIERS[tier])


def get_item_durability(item_type: ItemType) -> int:
    if item_type in CONSUMABLE_ITEMS:
        return 1
    if item_type in UNCONSUMABLE_DURABILITY_OVERRIDES:
        return UNCONSUMABLE_DURABILITY_OVERRIDES[item_type]
    return DEFAULT_UNCONSUMABLE_DURABILITY
