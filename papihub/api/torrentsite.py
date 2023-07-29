from abc import ABCMeta, abstractmethod
from typing import List, Optional

from papihub.api.types import Torrent, TorrentDetail, TorrentSiteUser


class TorrentSite(metaclass=ABCMeta):
    def __init(self):
        pass

    @abstractmethod
    async def list(self, timeout=None, cate_level1_list=None) -> List[Torrent]:
        pass

    @abstractmethod
    async def get_user(self, refresh=False) -> Optional[TorrentSiteUser]:
        pass

    @abstractmethod
    async def search(
            self,
            keyword=None,
            imdb_id=None,
            cate_level1_list: Optional[List] = None,
            free: Optional[bool] = False,
            page: Optional[int] = None,
            timeout=None
    ) -> List[Torrent]:
        pass

    @abstractmethod
    async def download_torrent(self, url, filepath):
        pass

    @abstractmethod
    async def get_detail(self, url) -> Optional[TorrentDetail]:
        pass
