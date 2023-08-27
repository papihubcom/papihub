from papihub.config.siteparserconfigloader import SiteParserConfigLoader
from papihub.exceptions import NotFoundParserException
from papihub.signals import site_init_signal
from papihub.models.sitemodel import AuthType, AuthConfig, SiteModel, SiteStatus


class SiteManager:
    """
    站点管理器
    """

    def __init__(self, site_parser_config_loader: SiteParserConfigLoader):
        self.site_parser_config_loader = site_parser_config_loader
        self.parser_config = site_parser_config_loader.load()

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
        # 发送站点初始化信号，异步做后续的处理
        site_init_signal.send(site_id)
