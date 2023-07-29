from typing import Optional, List

from papihub.api.auth import Auth
from papihub.api.torrentsite import TorrentSite
from papihub.api.types import TorrentDetail, Torrent, TorrentSiteUser


class NexusPhp(TorrentSite, Auth):

    async def auth_with_cookies(self, cookies_str: str):
        pass

    async def auth(self, username: str, password: str):
        pass

    async def list(self, timeout=None, cate_level1_list=None) -> List[Torrent]:
        pass

    async def get_user(self, refresh=False) -> Optional[TorrentSiteUser]:
        pass

    async def search(self, keyword=None, imdb_id=None, cate_level1_list: Optional[List] = None,
                     free: Optional[bool] = False, page: Optional[int] = None, timeout=None) -> List[Torrent]:
        pass

    async def download_torrent(self, url, filepath):
        pass

    async def get_detail(self, url) -> Optional[TorrentDetail]:
        pass
