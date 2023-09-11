from typing import Optional, Dict, List
from papihub import utils
from papihub.api.auth import Auth
from papihub.api.sites.nexusphp import NexusPhp
from papihub.api.torrentsite import TorrentSite
from papihub.config.siteparserconfigloader import SiteParserConfigLoader
from papihub.eventbus import bus, EVENT_SITE_INIT
from papihub.exceptions import NotFoundParserException, ParserException, SiteAuthenticationFailureException
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
        self.reload_site_instance()

    def reload_site_instance(self):
        """
        重新加载站点实例
        此处加载站点实例暂时不做强制验证，避免应用初始化过慢
        :return:
        """
        site_list = SiteModel.list()
        if not site_list:
            return
        for site in site_list:
            self.init_site(site.site_id, test_login=False)

    def get_instance(self, site_id: List[str]):
        """
        获取站点实例
        :param site_id: 站点唯一编号
        :return:
        """
        if not site_id:
            return []
        return [self.parser_instance.get(s) for s in site_id if self.parser_instance.get(s) is not None]

    def add(self, site_id: str, auth_type: AuthType, auth_config: AuthConfig):
        """
        添加站点配置信息
        配置会存储在数据库内，方便后期加载到程序
        :param site_id: 站点唯一编号
        :param auth_type: 授权类型
        :param auth_config: 授权详细配置
        :return:
        """
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

    def init_site(self, site_id: str, test_login: Optional[bool] = True):
        """
        初始化站信息
        初始化后会将状态同步存储到数据库内
        :param site_id: 站点唯一编号
        :param test_login: 是否测试登录
        :return:
        """
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

        try:
            if isinstance(torrent_site, Auth):
                if site_model.auth_type == AuthType.Cookies.value:
                    auth_config: CookieAuthConfig = CookieAuthConfig.from_json(site_model.auth_config)
                    torrent_site.auth_with_cookies(auth_config.cookies)
                    if test_login:
                        torrent_site.test_login()
                elif site_model.auth_type == AuthType.UserAuth.value:
                    cookie_store = CookieStoreModel.get_cookies(site_id)
                    auth = False
                    if cookie_store:
                        # 优先用现存cookie授权
                        torrent_site.auth_with_cookies(cookie_store.cookies)
                        if test_login:
                            auth = torrent_site.test_login()
                        else:
                            auth = True
                    if not auth:
                        # 如果已有cookie授权失败，使用用户名密码授权
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
                    raise SiteAuthenticationFailureException(site_id, parser_config.site_name)
        except Exception as e:
            site_model.site_status = SiteStatus.Error.value
            site_model.status_message = f'站点认证配置错误：{str(e)}'
            site_model.update()
            raise SiteAuthenticationFailureException(site_id, parser_config.site_name, e)
        self.parser_instance.update({site_id: torrent_site})
        SiteModel.update_status(site_id, SiteStatus.Active)
