import enum


class ItemType(enum.Enum):
    """
    Enum for Item Type
    """

    # Consumables
    # Common
    COOKIE = "COOKIE"
    COIN = "COIN"
    
    # Rare
    ENERGY_CELL = "ENERGY_CELL"
    BAG_OF_MONEY = "BAG_OF_MONEY"
    CACHE_CLEANER = "CACHE_CLEANER"

    # Epic
    MAINTENANCE_KIT = "MAINTENANCE_KIT"
    SACK_OF_MONEY = "SACK_OF_MONEY"
    REPAIR_KIT = "REPAIR_KIT"

    # Legendary
    TREASURE_CHEST = "TREASURE_CHEST"

    # Unconsumables
    # Rare
    CACHE = "CACHE"

    # Epic
    POWER_BANK = "POWER_BANK"
    PROCESSOR_PASTE = "PROCESSOR_PASTE"

    # Legendary
    OVERCLOCKING_DEVICE = "OVERCLOCKING_DEVICE"
    EXTERNAL_STORAGE = "EXTERNAL_STORAGE"
