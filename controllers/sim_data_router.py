from fastapi import APIRouter, HTTPException

from domain import sim_data_service
from domain.utils.sim_time_utils import format_sim_time_short


router = APIRouter(prefix="/sim_data", tags=["sim_data"])


@router.get("/sim_time")
async def get_sim_time() -> str:
    try:
        return format_sim_time_short(sim_data_service.get_sim_time())
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
