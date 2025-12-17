import traceback
from fastapi import APIRouter, HTTPException

from domain.dtos.policy_dto import PolicyDto
from domain.policy_service import fetch_active_policies


router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("/")
def get_active_policies() -> list[PolicyDto]:
    try:
        return fetch_active_policies()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
