from typing import List, Optional

import inject
from fastapi import APIRouter
from pydantic import BaseModel

from papihub.api.concurrenttorrentsite import ConcurrentTorrentSite
from papihub.api.types import CateLevel1
from papihub.common.response import json_200
from papihub.manager.sitemanager import SiteManager

router = APIRouter()


class SearchParam(BaseModel):
    site_id: Optional[List[str]]
    keyword: str
    imdb_id: Optional[str] = None
    cate_level1: Optional[List[CateLevel1]] = None


@router.post("/api/torrents/search")
def search(param: SearchParam):
    """
    搜索站点种子信息
    :param param:
    :return:
    """
    site_manager = inject.instance(SiteManager)
    cts = ConcurrentTorrentSite(
        torrent_sites=site_manager.get_instance(param.site_id)
    )
    results = cts.search(
        keyword=param.keyword,
        imdb_id=param.imdb_id,
        cate_level1=param.cate_level1
    )
    return json_200(data=results)
