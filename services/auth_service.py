import uuid

from sqlalchemy.orm import Session

from auth import create_access_token, hash_password, verify_password
from models import User
from services.exceptions import DuplicateError, UnauthorizedError


def register(name: str, email: str, password: str, db: Session) -> User:
    if db.query(User).filter(User.email == email).first():
        raise DuplicateError("El correo ya está registrado")
    user = User(
        id=str(uuid.uuid4()),
        name=name,
        email=email,
        password=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(email: str, password: str, db: Session) -> str:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise UnauthorizedError("Email o contraseña incorrectos")
    return create_access_token(data={"sub": str(user.id)})
