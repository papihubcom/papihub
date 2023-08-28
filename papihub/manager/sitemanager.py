from typing import Optional, Dict
from papihub import utils
from papihub.api.auth import Auth
from papihub.api.sites.nexusphp import NexusPhp
from papihub.api.torrentsite import TorrentSite
from papihub.config.siteparserconfigloader import SiteParserConfigLoader
from papihub.eventbus import bus, EVENT_SITE_INIT
from papihub.exceptions import NotFoundParserException, ParserException
from papihub.models import CookieStoreModel
from papihub.models.sitemodel import AuthType, AuthConfig, SiteModel, SiteStatus, CookieAuthConfig, UserAuthConfig


class SiteManager:
    """
    站点管理器
    """

    def __init__(self, site_parser_config_loader: SiteParserConfigLoader):
        self.parser_instance: Dict[str, TorrentSite] = {}
        self.site_parser_config_loader = site_parser_config_loader
        self.parser_config = site_parser_config_loader.load()

    def add(self, site_id: str, auth_type: AuthType, auth_config: AuthConfig):
        if site_id not in self.parser_config:
            raise NotFoundParserException(f'站点编号不存在：{site_id}')
        parser_config = self.parser_config[site_id]
        site = SiteModel.get_by_site_id(site_id)
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
        # 异步做后续的处理
        bus.emit(EVENT_SITE_INIT, site_id=site_id, threads=True)

    def init_site(self, site_id: str):
        site_model = SiteModel.get_by_site_id(site_id)
        if not site_model:
            site_model.site_status = SiteStatus.Error.value
            site_model.status_message = f'站点不存在：{site_id}'
            site_model.update()
            raise Exception(site_model.status_message)
        parser_config = self.parser_config[site_id]
        torrent_site: Optional[TorrentSite] = None
        if 'nexusphp' == parser_config.site_type:
            torrent_site = NexusPhp(parser_config)
        if not torrent_site:
            site_model.site_status = SiteStatus.Error.value
            site_model.status_message = f'站点类型不支持：{parser_config.site_type}'
            site_model.update()
            raise ParserException(site_model.status_message)
        if isinstance(torrent_site, Auth):
            if site_model.auth_type == AuthType.Cookies.value:
                auth_config: CookieAuthConfig = CookieAuthConfig.from_json(site_model.auth_config)
                torrent_site.auth_with_cookies(auth_config.cookies)
            elif site_model.auth_type == AuthType.UserAuth.value:
                cookie_store = CookieStoreModel.get_cookies(site_id)
                # todo 优先cookie登录，失败再重登录
                auth_config: UserAuthConfig = UserAuthConfig.from_json(site_model.auth_config)
                cookie_str = torrent_site.auth(auth_config.username, auth_config.password)
                expire_time = utils.parse_cookies_expire_time(cookie_str)
                ck_item = CookieStoreModel(
                    site_id=site_id,
                    cookies=cookie_str,
                    expire_time=expire_time
                )
                ck_item.save()
            else:
                site_model.site_status = SiteStatus.Error.value
                site_model.status_message = f'站点认证配置错误：{site_model.auth_config}'
                site_model.update()
                raise Exception(site_model.status_message)
        self.parser_instance.update({site_id: torrent_site})
        SiteModel.update_status(site_id, SiteStatus.Active)
