from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from typing import Optional, List

from papihub.databases import *


@dataclass
class AuthType(Enum):
    Cookies = 'cookies'
    UserAuth = 'user_auth'


@dataclass
@dataclass_json
class AuthConfig:
    auth_type: Optional[AuthType] = None
    user_agent: Optional[str] = None


@dataclass
class CookieAuthConfig(AuthConfig):
    cookies: Optional[str] = None


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
