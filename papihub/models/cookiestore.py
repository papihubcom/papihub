from typing import Optional, List

from papihub.databases import *


class CookieStore(BaseDBModel):
    """
    存储站点用的一些Cookie
    """
    __tablename__ = 'cookie_store'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    site_id = Column(String, comment='站点编号', nullable=False)
    cookies = Column(String, comment='Cookie字符串', nullable=False)
    expire_time = Column(DateTime, nullable=False, default=datetime.datetime.now, comment='过期时间')
