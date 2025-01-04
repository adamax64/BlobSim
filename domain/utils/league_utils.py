INACTIVE_SEASON = 0
MINIMAL_SEASON = 4
SHORT_SEASON = 8
HALF_SEASON = 12
MEDIUM_SEASON = 16
LONG_SEASON = 20
MAXIMAL_SEASON = 24


def get_number_of_rounds_by_size(league_size: int) -> int:
    if league_size >= 22:
        return MAXIMAL_SEASON
    if league_size >= 18:
        return LONG_SEASON
    if league_size >= 14:
        return MEDIUM_SEASON
    if league_size >= 11:
        return HALF_SEASON
    if league_size >= 8:
        return SHORT_SEASON
    if league_size >= 5:
        return MINIMAL_SEASON
    return INACTIVE_SEASON


def get_epoch_cycle_by_level(level: int) -> int:
    if level == 1:
        return 3
    if level == 2:
        return 2
    if level == 3:
        return 1
    if level == 0:
        return 0
    return -1
