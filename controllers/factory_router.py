from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
import traceback

from domain.dtos.factory_progress_dto import FactoryProgressDto
from domain.dtos.name_suggestion_dto import NameSuggestionDto
from domain.exceptions.name_occupied_exception import NameOccupiedException
from domain.sim_data_service import (
    get_factory_progress as service_get_factory_progress,
    get_weather as service_get_weather,
    get_wind as service_get_wind,
)
from domain.weather_service import get_output_chances
from domain.naming_service import (
    get_name_suggestions as service_get_name_suggestions,
    save_name_suggestion as service_save_name_suggestion,
    update_name_suggestion as service_update_name_suggestion,
)
from domain.utils.constants import BLOB_CREATION_RESOURCES
from .auth_dependency import require_auth


router = APIRouter(prefix="/factory", tags=["factory"])


@router.get("/progress")
def get_factory_progress() -> FactoryProgressDto:
    try:
        weather = service_get_weather()
        wind = service_get_wind()
        solar_efficiency, wind_efficiency, hydro_efficiency = get_output_chances(weather, wind)
        return FactoryProgressDto(
            progress=service_get_factory_progress() / BLOB_CREATION_RESOURCES,
            solar_efficiency=solar_efficiency,
            wind_efficiency=wind_efficiency,
            hydro_efficiency=hydro_efficiency,
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.get("/name-suggestions")
def get_name_suggestions() -> list[NameSuggestionDto]:
    try:
        return service_get_name_suggestions()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/save-name-suggestion")
def save_name_suggestion(first_name: str, last_name: str, _=Depends(require_auth)) -> Response:
    if first_name is None or first_name == "" or last_name is None or last_name == "":
        raise HTTPException(status_code=400, detail="FIRST_NAME_AND_LAST_NAME_REQUIRED")
    try:
        service_save_name_suggestion(first_name=first_name, last_name=last_name)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NameOccupiedException:
        raise HTTPException(status_code=409, detail="NAME_ALREADY_OCCUPIED")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/update-name-suggestion")
def update_name_suggestion(id: int, first_name: str, _=Depends(require_auth)) -> Response:
    """ Updates the first name of a child name suggestion """
    try:
        service_update_name_suggestion(id=id, first_name=first_name)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
