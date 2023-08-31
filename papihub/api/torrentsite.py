from abc import ABCMeta, abstractmethod
from typing import List, Optional

from papihub.api.types import Torrent, TorrentDetail, TorrentSiteUser
from papihub.config.types import TorrentSiteParserConfig


class TorrentSite(metaclass=ABCMeta):
    """
    种子站点抓取接口
    """
    parser_config: TorrentSiteParserConfig

    @abstractmethod
    def list(self, timeout=None, cate_level1_list=None) -> List[Torrent]:
        """
        获取种子列表
        :param timeout: 超时信息
        :param cate_level1_list: 一级种子分类信息
        :return:
        """
        pass

    @abstractmethod
    def get_user(self, refresh=False) -> Optional[TorrentSiteUser]:
        """
        获取用户信息
        :param refresh:
        :return:
        """
        pass

    @abstractmethod
    def search(
            self,
            keyword: Optional[str] = None,
            imdb_id: Optional[str] = None,
            cate_level1_list: Optional[List] = None,
            free: Optional[bool] = False,
            page: Optional[int] = None,
            timeout: Optional[int] = None
    ) -> List[Torrent]:
        """
        搜索种子
        :param keyword:
        :param imdb_id:
        :param cate_level1_list:
        :param free:
        :param page:
        :param timeout:
        :return:
        """
        pass

    @abstractmethod
    def download_torrent(self, url, filepath):
        """
        下载种子
        :param url:
        :param filepath:
        :return:
        """
        pass

    @abstractmethod
    def get_detail(self, url) -> Optional[TorrentDetail]:
        """
        获取种子详情信息
        :param url:
        :return:
        """
        pass
