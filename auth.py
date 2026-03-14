import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#limita la contraseña a 72 bytes
_MAX_BCRYPT_BYTES = 72


def _truncate_password(password: str) -> str:
    """Trunca la contraseña a 72 bytes para evitar problemas con bcrypt"""
    encoded = password.encode("utf-8")
    if len(encoded) <= _MAX_BCRYPT_BYTES:
        return password
    return encoded[:_MAX_BCRYPT_BYTES].decode("utf-8", errors="ignore") or password[:1]


def hash_password(password: str) -> str:
    """Hashea la contraseña truncada a 72 bytes"""
    return pwd_context.hash(_truncate_password(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica la contraseña truncada a 72 bytes contra el hash almacenado"""
    return pwd_context.verify(_truncate_password(plain_password), hashed_password)


def create_access_token(data: dict) -> str:
    """Crea un token JWT con una expiración"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict | None:
    """Verifica el token JWT y devuelve su payload si es válido"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
