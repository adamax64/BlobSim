from fastapi import APIRouter

from domain import sim_data_service


router = APIRouter(prefix="/sim_data", tags=["sim_data"])


@router.get("/sim_time")
async def get_sim_time() -> int:
    return sim_data_service.get_sim_time()
