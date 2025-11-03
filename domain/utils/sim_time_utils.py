from domain.dtos.sim_time_dto import SimTimeDto
from domain.utils.constants import (
    CYCLES_PER_EON,
    CYCLES_PER_EPOCH,
    CYCLES_PER_SEASON,
    EPOCHS_PER_SEASON,
)


def convert_to_sim_time(sim_time: int) -> SimTimeDto:
    """
    Convert simulation time to a human-readable format.
    """
    return SimTimeDto(
            eon=int(sim_time / CYCLES_PER_EON),
            season=int(sim_time / CYCLES_PER_SEASON + 1),
            epoch=int(sim_time / CYCLES_PER_EPOCH) % EPOCHS_PER_SEASON,
            cycle=sim_time % CYCLES_PER_EPOCH
        )


def get_eon(time: int) -> int:
    return int(time / CYCLES_PER_EON)


def get_season(time: int) -> int:
    return int(time / CYCLES_PER_SEASON) + 1


def is_season_start(time: int) -> bool:
    return time % CYCLES_PER_SEASON == 0


def is_season_end(time: int) -> bool:
    return time % CYCLES_PER_SEASON == CYCLES_PER_SEASON - 1


def get_sim_time_from(season: int, epoch: int, cycle: int) -> int:
    return (season - 1) * CYCLES_PER_SEASON + epoch * CYCLES_PER_EPOCH + cycle


def format_sim_time_short(time: int) -> str:
    return f"{int(time / CYCLES_PER_SEASON) + 1}. {int(time / CYCLES_PER_EPOCH) % EPOCHS_PER_SEASON:2d} - {time % CYCLES_PER_EPOCH}"
