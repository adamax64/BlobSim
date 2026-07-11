from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
import traceback

from pydantic import BaseModel

from domain.blob_services.blob_fetching_service import (
    fetch_blob_by_id,
    get_blobs_by_activities,
    get_current_grandmaster,
)
from domain.blob_services.blob_service import (
    get_all_blobs,
    create_blob as service_create_blob,
)
from domain.dtos.blob_dtos.blob_stats_dto import BlobStatsDto
from domain.enums.activity_type import ActivityType
from domain.exceptions.name_occupied_exception import NameOccupiedException
from domain.exceptions.no_grandmaster_found_exception import NoGrandmasterFoundException
from .auth_dependency import require_auth

router = APIRouter(prefix="/blobs", tags=["blobs"])


class BlobsByActivityRequestDto(BaseModel):
    activities: list[ActivityType]


@router.get("/all", response_model=list[BlobStatsDto])
def get_all(
    name_search: str | None = None, show_dead: bool = False
) -> list[BlobStatsDto]:
    try:
        return get_all_blobs(name_search=name_search, show_dead=show_dead)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.get("/:blob_id", response_model=BlobStatsDto)
def get_blob(blob_id: int) -> BlobStatsDto:
    try:
        return fetch_blob_by_id(blob_id)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.get("/grandmaster", response_model=BlobStatsDto)
def get_grandmaster() -> BlobStatsDto:
    try:
        return get_current_grandmaster()
    except NoGrandmasterFoundException as nge:
        raise HTTPException(status_code=404, detail=str(nge))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/blobs_by_activities", response_model=list[BlobStatsDto])
def get_by_activities(resuest: BlobsByActivityRequestDto) -> list[BlobStatsDto]:
    try:
        return get_blobs_by_activities(activities=resuest.activities)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/create")
def create_blob(
    first_name: str,
    last_name: str,
    parent_id: int | None = None,
    _=Depends(require_auth),
) -> Response:
    try:
        service_create_blob(
            first_name=first_name, last_name=last_name, parent_id=parent_id
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NameOccupiedException:
        raise HTTPException(status_code=409, detail="NAME_ALREADY_OCCUPIED")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
