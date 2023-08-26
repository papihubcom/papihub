from typing import Dict

from papihub.config.siteparserconfigloader import SiteParserConfigLoader
from papihub.config.types import ParserConfig
from papihub.exceptions import NotFoundParserException
from papihub.models.sitemodel import AuthType, AuthConfig, SiteModel, SiteStatus


class SiteManager:
    def __init__(self, parser_config: Dict[str, ParserConfig]):
        self.parser_config = parser_config

    def add(self, site_id: str, auth_type: AuthType, auth_config: AuthConfig):
        if site_id not in self.parser_config:
            raise NotFoundParserException(f'站点编号不存在：{site_id}')
        parser_config = self.parser_config[site_id]
        site = SiteModel.query().filter(SiteModel.site_id == site_id).first()
        if site:
            raise Exception(f'站点已存在：{site_id}')
        site = SiteModel(
            site_id=site_id,
            display_name=parser_config.site_name,
            auth_type=auth_type.value,
            auth_config=auth_config.to_json(),
            site_status=SiteStatus.Pending.value
        )
        site.save()
        # todo 添加站点后，异步验证站点是否可用
