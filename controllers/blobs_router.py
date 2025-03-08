from fastapi import APIRouter

from domain.blob_service import get_all_blobs
from domain.dtos.blob_stats_dto import BlobStatsDto


router = APIRouter(prefix="/blobs", tags=["blobs"])


@router.get("/all", response_model=list[BlobStatsDto])
def get_all(
    name_search: str | None = None, show_dead: bool = False
) -> list[BlobStatsDto]:
    try:
        return get_all_blobs(name_search=name_search, show_dead=show_dead)
    except Exception as e:
        print(e.with_traceback(None))
