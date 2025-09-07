import enum


class ActivityTypeDbo(enum.Enum):
    """
    Enum for Activity Type
    """
    EVENT = 'EVENT'
    MAINTENANCE = 'MAINTENANCE'

    PRACTICE = 'PRACTICE'
    LABOUR = 'LABOUR'
    IDLE = 'IDLE'
