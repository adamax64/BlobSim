import traceback
from fastapi import APIRouter, HTTPException

from domain.dtos.news_dto import NewsDto
from domain.news_services.fetch_news_service import fetch_all_news


router = APIRouter(prefix="/news", tags=["news"])


@router.get("/")
def get_news() -> list[NewsDto]:
    try:
        return fetch_all_news()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
