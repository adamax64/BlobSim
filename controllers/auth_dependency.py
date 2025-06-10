from fastapi import Depends
from .auth_router import get_current_user


def require_auth(current_user: str = Depends(get_current_user)):
    return current_user
