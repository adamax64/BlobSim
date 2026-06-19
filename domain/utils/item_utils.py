import random

from data.model.item_type import ItemType

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
        ItemType.OVERCLOCKING_SCRIPT,
        ItemType.EXTERNAL_STORAGE,
    ),
}

RARITY_WEIGHTS = [60, 20, 16, 4]


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
