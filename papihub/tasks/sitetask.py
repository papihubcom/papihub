import logging

import inject

from papihub.eventbus import bus, EVENT_SITE_INIT
from papihub.manager.sitemanager import SiteManager

_LOGGER = logging.getLogger(__name__)


@bus.on(EVENT_SITE_INIT)
def on_site_init(site_id: str):
    """
    接收站点初始化事件对站点授权信息进行验证，实例初始化。
    :param site_id: 站点唯一编号
    :return:
    """
    _LOGGER.info("站带初始化事件：%s", site_id)
    site_manager = inject.instance(SiteManager)
    site_manager.init_site(site_id)
