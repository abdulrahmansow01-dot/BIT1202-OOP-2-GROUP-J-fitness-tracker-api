from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth import decode_access_token
from crud import get_user_by_email
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def get_current_active_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        token_data = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    user = await get_user_by_email(db, token_data.email)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user", headers={"WWW-Authenticate": "Bearer"})
    return user
