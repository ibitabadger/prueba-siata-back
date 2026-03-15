from fastapi import Depends, HTTPException, Request, status

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session as DBSession
from database import SessionLocal
from auth import verify_token
from models import User

security = HTTPBearer()


def get_db():
    """Abre el recurso y lo entrega temporalmente(Patrón generador)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: DBSession = Depends(get_db),
) -> User:
    """Obtiene el usuario actual a partir del token de autenticación."""
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )
    return user


def require_auth_for_protected_paths(
    request: Request,
    db: DBSession = Depends(get_db),
) -> User | None:
    """
    - Deja pasar sin token: /, /docs, /redoc, /openapi.json
    - Para el resto exige Authorization: Bearer <token>.
    """
    path = request.url.path
    public_paths = {"/", "/docs", "/redoc", "/openapi.json"}
    if path in public_paths or path.startswith("/api/auth"):
        return None

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación requerido",
        )

    token = auth_header.split(" ", 1)[1].strip()
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    return user

