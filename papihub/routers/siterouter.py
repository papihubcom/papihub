import inject
from fastapi import APIRouter, Depends

from papihub.auth import get_current_user
from papihub.common.response import json_200
from pydantic import BaseModel

from papihub.manager.sitemanager import SiteManager
from papihub.models.sitemodel import AuthType, CookieAuthConfig, UserAuthConfig, SiteModel
from papihub.models.usermodel import UserModel

router = APIRouter()


class AddParam(BaseModel):
    """
    添加站点接口的参数
    """
    site_id: str
    auth_type: str
    auth_config: dict


@router.get("/api/site/list_parsers")
def list_parsers():
    site_manager = inject.instance(SiteManager)
    return json_200(
        message='获取站点解析器配置成功',
        data=[{
            'site_id': x.site_id,
            'site_name': x.site_name,
            'domain': x.domain,
            'site_type': x.site_type,
            'config_type': x.config_type,
            'encoding': x.encoding,
        } for x in site_manager.parser_config.values()]
    )


@router.get("/api/site/list")
def list():
    site_list = SiteModel.list()
    site_manager = inject.instance(SiteManager)
    results = []
    for x in site_list:
        config = site_manager.parser_config.get(x.site_id)
        results.append({
            'site_id': x.site_id,
            'site_name': x.display_name,
            'auth_type': x.auth_type,
            'site_status': x.site_status,
            'status_message': x.status_message,
            'domain': config.domain,
            'last_active_time': x.last_active_time
        })
    return json_200(
        message='获取站点配置成功',
        data=results
    )


@router.post("/api/site/add")
def add(param: AddParam, user: UserModel = Depends(get_current_user)):
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
