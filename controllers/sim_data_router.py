from fastapi import APIRouter, HTTPException, Depends

from domain import sim_data_service
from domain.blob_service import update_blobs
from domain.dtos.sim_time_dto import SimTimeDto
from domain.utils.sim_time_utils import convert_to_sim_time
from .auth_dependency import require_auth


router = APIRouter(prefix="/sim_data", tags=["sim_data"])


@router.get("/sim_time")
async def get_sim_time() -> SimTimeDto:
    try:
        sim_time = sim_data_service.get_sim_time()
        return convert_to_sim_time(sim_time)
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/simulate")
def progress(_=Depends(require_auth)):
    """
    Simulate the progress of the simulation and update blobs.
    """
    try:
        update_blobs()
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"Error while updating blobs: {e.with_traceback(None)}")

    try:
        sim_data_service.progress_simulation()
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"Error while updating simulation progress: {e.with_traceback(None)}")

    return
