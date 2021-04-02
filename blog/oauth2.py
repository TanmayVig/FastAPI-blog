from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from . import token
from blog import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
async def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verify_token(data,credentials_exception)

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user
