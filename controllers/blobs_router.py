from fastapi import APIRouter, HTTPException, Response, status

from domain.blob_service import get_all_blobs, create_blob as service_create_blob
from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.exceptions.name_occupied_exception import NameOccupiedException


router = APIRouter(prefix="/blobs", tags=["blobs"])


@router.get("/all", response_model=list[BlobStatsDto])
def get_all(
    name_search: str | None = None, show_dead: bool = False
) -> list[BlobStatsDto]:
    try:
        return get_all_blobs(name_search=name_search, show_dead=show_dead)
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/create")
def create_blob(first_name: str, last_name: str, parent_id: int | None = None) -> Response:
    try:
        service_create_blob(first_name=first_name, last_name=last_name, parent_id=parent_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NameOccupiedException:
        raise HTTPException(status_code=409, detail="NAME_ALREADY_OCCUPIED")
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
