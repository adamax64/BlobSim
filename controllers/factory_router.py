from fastapi import APIRouter, HTTPException

from controllers.validations import validate_blob_name
from domain.dtos.name_suggestion_dto import NameSuggestionDto
from domain.exceptions.name_occupied_exception import NameOccupiedException
from domain.sim_data_service import get_factory_progress as service_get_factory_progress
from domain.naming_service import get_name_suggestions as service_get_name_suggestions, save_name_suggestion as service_save_name_suggestion
from domain.utils.constants import BLOB_CREATION_RESOURCES
from fastapi import status
from fastapi.responses import Response


router = APIRouter(prefix="/factory", tags=["factory"])


@router.get("/progress")
def get_factory_progress() -> float:
    try:
        return service_get_factory_progress() / BLOB_CREATION_RESOURCES
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.get("/name-suggestions")
def get_name_suggestions() -> list[NameSuggestionDto]:
    try:
        return service_get_name_suggestions()
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/save-name-suggestion")
def save_name_suggestion(name: str) -> Response:
    validate_blob_name(name)

    try:
        service_save_name_suggestion(name=name)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NameOccupiedException:
        raise HTTPException(status_code=409, detail="NAME_ALREADY_OCCUPIED")
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
