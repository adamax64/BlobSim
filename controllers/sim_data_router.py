from fastapi import APIRouter

from domain import sim_data_service
from domain.utils.constants import (
    CYCLES_PER_EPOCH,
    CYCLES_PER_SEASON,
    EPOCHS_PER_SEASON,
)


router = APIRouter(prefix="/sim_data", tags=["sim_data"])


@router.get("/sim_time")
async def get_sim_time() -> str:
    return format_sim_time_short(sim_data_service.get_sim_time())


def format_sim_time_short(time: int) -> str:
    return f"{int(time / CYCLES_PER_SEASON) + 1}. {int(time / CYCLES_PER_EPOCH) % EPOCHS_PER_SEASON:2d} - {time % CYCLES_PER_EPOCH}"
