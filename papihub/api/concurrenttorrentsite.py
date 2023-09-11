import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

from papihub.api.torrentsite import TorrentSite
from papihub.api.types import Torrent
from papihub.exceptions import SiteApiErrorException

_LOGGER = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=50)


class ConcurrentTorrentSite:
    """
    并行种子站点操作类
    传入很多站点实例后，开启多线程并行处理
    """

    def __init__(self, torrent_sites: List[TorrentSite]):
        if not torrent_sites:
            raise SiteApiErrorException('没有可用的站点')
        self.torrent_sites = torrent_sites

    def search(
            self,
            keyword: str,
            imdb_id: Optional[str],
            cate_level1: Optional[List[str]]
    ):
        results: List[Torrent] = []
        futures = [executor.submit(lambda: s.search(
            keyword=keyword,
            imdb_id=imdb_id,
            cate_level1_list=cate_level1
        )) for s in self.torrent_sites]
        for future in futures:
            try:
                r = future.result()
                if not r:
                    continue
                results.extend(r)
            except Exception as e:
                _LOGGER.error(e)
        return results
