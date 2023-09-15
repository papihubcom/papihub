from datetime import timedelta
from typing import Optional

from fastapi import Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from papihub.auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from papihub.common.response import json_with_status, json_200
from papihub.models.usermodel import UserModel

router = APIRouter()


def auth(username: str, password: str) -> Optional[UserModel]:
    user = UserModel.get_by_username(username)
    if not user:
        return
    # 密码要加盐，防范彩虹表攻击
    if not verify_password(password, user.password):
        return
    return user


@router.get("/api/user/profile")
def profile(user: UserModel = Depends(get_current_user)):
    return json_200(data=user)


@router.post("/api/user/get_token")
def get_token(form: OAuth2PasswordRequestForm = Depends()):
    user = auth(form.username, form.password)
    if not user:
        return json_with_status(status.HTTP_401_UNAUTHORIZED, message='用户名或密码错误')
    token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return json_200(data={"access_token": token, "token_type": "bearer"}, message='登录成功')
