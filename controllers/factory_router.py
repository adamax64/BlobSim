from fastapi import APIRouter

from domain.dtos.name_suggestion_dto import NameSuggestionDto
from domain.sim_data_service import get_factory_progress as service_get_factory_progress
from domain.naming_service import get_name_suggestions as service_get_name_suggestions
from domain.utils.constants import BLOB_CREATION_RESOURCES


router = APIRouter(prefix="/factory", tags=["factory"])


@router.get("/progress")
def get_factory_progress() -> float:
    try:
        return service_get_factory_progress() / BLOB_CREATION_RESOURCES
    except Exception as e:
        print(e.with_traceback(None))


@router.get("/name-suggestions")
def get_name_suggestions() -> list[NameSuggestionDto]:
    try:
        return service_get_name_suggestions()
    except Exception as e:
        print(e.with_traceback(None))
