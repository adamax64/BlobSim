from fastapi import APIRouter

from domain import sim_data_service
from domain.utils.sim_time_utils import format_sim_time_short


router = APIRouter(prefix="/sim_data", tags=["sim_data"])


@router.get("/sim_time")
async def get_sim_time() -> str:
    return format_sim_time_short(sim_data_service.get_sim_time())
