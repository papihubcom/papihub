from typing import Optional, List

from papihub.databases import *


class CookieStoreModel(BaseDBModel):
    """
    存储站点用的一些Cookie
    """
    __tablename__ = 'cookie_store'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    site_id = Column(String, comment='站点编号', nullable=False)
    cookies = Column(String, comment='Cookie字符串', nullable=False)
    expire_time = Column(DateTime, nullable=False, default=datetime.datetime.now, comment='过期时间')

    @staticmethod
    def get_cookies(site_id: str) -> Optional["CookieStoreModel"]:
        """
        根据站点唯一编号获取存储的cookie信息，只返回首条结果
        :param site_id:
        :return:
        """
        return CookieStoreModel.query().filter(
            (CookieStoreModel.site_id == site_id) & (CookieStoreModel.expire_time > datetime.datetime.now())).first()
