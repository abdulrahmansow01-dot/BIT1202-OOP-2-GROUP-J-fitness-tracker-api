from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings
from schemas import TokenData
from crud import get_user_by_email

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
ALGORITHM = getattr(settings, 'algorithm', "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, 'access_token_expire_minutes', 60)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    print("PLAIN PASSWORD:", plain_password)
    print("HASHED PASSWORD:", hashed_password[:50])
    
    result = pwd_context.verify(plain_password, hashed_password)
    print("VERIFY RESULT:", result)
    
    return result

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> TokenData:
    credentials_exception = JWTError("Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except JWTError as exc:
        raise exc


async def authenticate_user(db, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
