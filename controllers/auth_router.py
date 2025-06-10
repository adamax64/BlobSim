from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from domain.login_service import validate_credentials
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import Optional


# Load environment variables
load_dotenv()


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Get secret key from environment variables, with a fallback for development
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-do-not-use-in-production")
ALGORITHM = "HS256"


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if "exp" in payload and datetime.now() > datetime.fromtimestamp(payload["exp"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError:
        raise credentials_exception


@router.post("/login", response_model=Token)
def login(request: LoginRequest):
    try:
        is_valid = validate_credentials(request.username, request.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        # Create access token
        access_token_expires = timedelta(hours=1)
        access_token = create_access_token(
            data={"sub": request.username}, expires_delta=access_token_expires
        )
        return {"token": access_token}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/validate")
async def validate_token(current_user: str = Depends(get_current_user)):
    return {"email": current_user}
