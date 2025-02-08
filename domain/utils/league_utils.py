INACTIVE_SEASON = 0
MINIMAL_SEASON = 4
SHORT_SEASON = 8
HALF_SEASON = 12
MEDIUM_SEASON = 16
LONG_SEASON = 20
MAXIMAL_SEASON = 24

TINY_FIELD = 5
SMALL_FIELD = 8
NEAR_HALF_FIELD = 11
MEDIUM_FIELD = 14
LARGE_FIELD = 18
HUGE_FIELD = 22


def get_race_duration_by_size(league_size: int) -> int:
    if league_size >= HUGE_FIELD:
        return 120
    if league_size >= LARGE_FIELD:
        return 110
    if league_size >= MEDIUM_FIELD:
        return 100
    if league_size >= NEAR_HALF_FIELD:
        return 90
    if league_size >= SMALL_FIELD:
        return 75
    if league_size >= TINY_FIELD:
        return 60


def get_number_of_rounds_by_size(league_size: int) -> int:
    if league_size >= HUGE_FIELD:
        return MAXIMAL_SEASON
    if league_size >= LARGE_FIELD:
        return LONG_SEASON
    if league_size >= MEDIUM_FIELD:
        return MEDIUM_SEASON
    if league_size >= NEAR_HALF_FIELD:
        return HALF_SEASON
    if league_size >= SMALL_FIELD:
        return SHORT_SEASON
    if league_size >= TINY_FIELD:
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
