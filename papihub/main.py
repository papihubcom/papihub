"""
程序启动入口类
"""
import json
import logging.config
import os

from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from papihub.common.logging import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

import inject

from papihub.config.siteparserconfigloader import SiteParserConfigLoader
from papihub.manager.sitemanager import SiteManager

import httpx
import uvicorn
from starlette.exceptions import HTTPException
from fastapi import FastAPI
from papihub.databases import create_all

from papihub.common.response import json_200, json_500, json_with_status
from papihub.routers import torrentsrouter
from papihub.routers import siterouter
from papihub.routers import userrouter
from papihub.models import *
from papihub.tasks import *

log = logging.getLogger(__name__)

# 初始化ORM框架
create_all()

app = FastAPI()

# 加载所有fastapi的接口路由
app.include_router(torrentsrouter.router)
app.include_router(siterouter.router)
app.include_router(userrouter.router)


@app.get("/")
async def root():
    """
    默认首页
    :return:
    """
    return json_200(message='papihub server')


@app.exception_handler(RequestValidationError)
async def unprocessable_entity_handler(request, exc: RequestValidationError):
    return json_with_status(
        status_code=422,
        message='参数错误',
        data=dict(exc.errors())
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return json_with_status(status_code=exc.status_code, message=exc.detail)


@app.exception_handler(httpx.HTTPStatusError)
async def http_status_exception_handler(request, e: httpx.HTTPStatusError):
    msg = e.response.json().get('error', {}).get('message')
    log.error('http status exception: ' + msg, exc_info=True)
    return json_500(message=msg)


@app.exception_handler(Exception)
async def universal_exception_handler(request, exc):
    log.error('universal_exception_handler', exc_info=True)
    return json_500(message=str(exc))


def config(binder):
    """
    依赖注入机制的初始化
    所有通过inject使用的对象，需要提前再此绑定
    :param binder:
    :return:
    """
    loader = SiteParserConfigLoader(conf_path=os.path.join(os.environ.get('WORKDIR'), 'conf', 'parser'))
    binder.bind(SiteParserConfigLoader, loader)
    binder.bind(SiteManager, SiteManager(loader))


def init_biz_data():
    """
    初始化业务数据
    :return:
    """
    from papihub.models.usermodel import UserModel
    list_users = UserModel.query().all()
    if not list_users:
        log.info("初始化用户：admin 密码：papiadmin 请尽快登录后修改密码")
        from papihub.auth import get_password_hash
        user = UserModel(
            nickname="默认管理员",
            username='admin',
            password=get_password_hash("papiadmin"),
        )
        user.save()


if __name__ == "__main__":
    # 加载公共全局依赖
    inject.configure(config)
    init_biz_data()
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("WEB_PORT", 8000))
