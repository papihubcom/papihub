import inject
from fastapi import APIRouter

from papihub.common.response import json_200
from pydantic import BaseModel

from papihub.manager.sitemanager import SiteManager
from papihub.models.sitemodel import AuthType, CookieAuthConfig, UserAuthConfig

router = APIRouter()


class AddParam(BaseModel):
    """
    添加站点接口的参数
    """
    site_id: str
    auth_type: str
    auth_config: dict


@router.post("/api/site/add")
def add(param: AddParam):
    """
    添加站点信息到数据库
    :param param:
    :return:
    """
    site_manager = inject.instance(SiteManager)
    auth_type = AuthType.from_str(param.auth_type)
    auth_config = None
    if auth_type is AuthType.Cookies:
        auth_config = CookieAuthConfig.from_dict(param.auth_config)
    elif auth_type is AuthType.UserAuth:
        auth_config = UserAuthConfig.from_dict(param.auth_config)
    site_manager.add(
        site_id=param.site_id,
        auth_type=auth_type,
        auth_config=auth_config
    )
    return json_200(
        message='添加站点配置成功',
    )
