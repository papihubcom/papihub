from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from typing import Optional, List

from papihub.databases import *


@dataclass
class AuthType(Enum):
    Cookies = 'cookies'
    UserAuth = 'user_auth'

    @staticmethod
    def from_str(value: str):
        if value == 'cookies':
            return AuthType.Cookies
        elif value == 'user_auth':
            return AuthType.UserAuth
        else:
            raise NotImplementedError


@dataclass_json
@dataclass
class AuthConfig:
    user_agent: Optional[str] = None


@dataclass_json
@dataclass
class CookieAuthConfig(AuthConfig):
    cookies: Optional[str] = None


@dataclass_json
@dataclass
class UserAuthConfig(AuthConfig):
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class SiteStatus(Enum):
    Pending = 'pending'
    Active = 'active'
    Error = 'error'


class SiteModel(BaseDBModel):
    """
    站点信息管理
    """
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    site_id = Column(String, comment='站点编号', nullable=False)
    display_name = Column(String, comment='站点显示名称', nullable=False)
    auth_type = Column(String, comment='站点认证类型', nullable=False)
    auth_config = Column(String, comment='站点认证配置', nullable=False)
    site_status = Column(String, comment='站点状态', nullable=False, default='pending')
    status_message = Column(String, comment='状态信息', nullable=True)
    last_active_time = Column(DateTime, nullable=False, default=datetime.datetime.now)

    @staticmethod
    def list() -> List["SiteModel"]:
        """
        获取所有站点信息
        :return:
        """
        return SiteModel.query().all()

    @staticmethod
    def get_by_site_id(site_id: str) -> "SiteModel":
        """
        根据站点唯一编号获取站点信息
        :param site_id:
        :return:
        """
        return SiteModel.query().filter(SiteModel.site_id == site_id).first()

    @staticmethod
    def update_status(site_id: str, status: SiteStatus, message: Optional[str] = None):
        """
        更新站点状态
        :param site_id: 站点唯一编号
        :param status: 状态码
        :param message: 状态相关消息
        :return:
        """
        site = SiteModel.get_by_site_id(site_id)
        if site:
            site.site_status = status.value
            site.status_message = message
            site.update()
