from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db
from schemas import TokenResponse, UserLogin, UserRegister, UserResponse
from services.auth_service import login as login_svc, register as register_svc
from services.exceptions import DuplicateError, UnauthorizedError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(body: UserRegister, db: Session = Depends(get_db)):
    try:
        return register_svc(body.name, body.email, body.password, db)
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(body: UserLogin, db: Session = Depends(get_db)):
    try:
        token = login_svc(body.email, body.password, db)
        return TokenResponse(access_token=token)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
