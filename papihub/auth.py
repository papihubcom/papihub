import datetime
import time
from datetime import timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from papihub.models.usermodel import UserModel

# 一周过期，单位分钟
ACCESS_TOKEN_EXPIRE_MINUTES = 10080

# openssl rand -hex 32 生成 secret_key
SECRET_KEY = "4f30cdb27ed3002c32b289371dd5897e73178719432f6b27bbd1747169a6e0b8"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/get_token")

# 密码加盐
PWD_SALT = "d3A^FQh8**!q"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password + PWD_SALT)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password + PWD_SALT, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.datetime.now() + expires_delta
    else:
        expire = datetime.datetime.now() + timedelta(minutes=60)
    data = {**data, "exp": expire}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
):
    authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="验证信息无效",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        expires = payload.get("exp")
        if expires < time.time():
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = UserModel.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user
