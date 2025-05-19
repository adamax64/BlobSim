from dataclasses import dataclass
from fastapi import APIRouter, HTTPException

from domain import sim_data_service
from domain.blob_service import update_blobs
from domain.utils.constants import CYCLES_PER_EON, CYCLES_PER_EPOCH, CYCLES_PER_SEASON, EPOCHS_PER_SEASON


router = APIRouter(prefix="/sim_data", tags=["sim_data"])


@dataclass
class SimTime:
    eon: int
    season: int
    epoch: int
    cycle: int


@router.get("/sim_time")
async def get_sim_time() -> SimTime:
    try:
        sim_time = sim_data_service.get_sim_time()
        return SimTime(
            eon=int(sim_time / CYCLES_PER_EON),
            season=int(sim_time / CYCLES_PER_SEASON + 1),
            epoch=int(sim_time / CYCLES_PER_EPOCH) % EPOCHS_PER_SEASON,
            cycle=sim_time % CYCLES_PER_EPOCH
        )
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/simulate")
def progress():
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
