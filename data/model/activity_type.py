import enum


class ActivityTypeDbo(enum.Enum):
    """
    Enum for Activity Type
    """
    EVENT = 'EVENT'
    MAINTENANCE = 'MAINTENANCE'

    INTENSE_TRAINING = 'INTENSE_TRAINING'
    PRACTICE = 'PRACTICE'
    LABOUR = 'LABOUR'
    IDLE = 'IDLE'

    ADMINISTRATION = 'ADMINISTRATION'
    MINING = 'MINING'
