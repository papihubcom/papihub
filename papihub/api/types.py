import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class TorrentSiteUser:
    uid: Optional[int] = 0
    username: Optional[str] = 'unknown'
    user_group: Optional[str] = 'unknown'
    share_ratio: Optional[float] = 0
    uploaded: Optional[float] = 0
    downloaded: Optional[float] = 0
    seeding: Optional[int] = 0
    leeching: Optional[int] = 0
    vip_group: Optional[bool] = False


@dataclass
class CateLevel1(str, Enum):
    Movie = '电影'
    TV = '剧集'
    Documentary = '纪录片'
    Anime = '动漫'
    Music = '音乐'
    Game = '游戏'
    AV = '成人'
    Other = '其他'

    @staticmethod
    def get_type(enum_name: str) -> Optional["CateLevel1"]:
        for item in CateLevel1:
            if item.name == enum_name:
                return item
        return None


@dataclass
class Torrent:
    # 站点编号
    site_id: Optional[str] = None
    # 种子编号
    id: Optional[str] = None
    # 种子名称
    name: Optional[str] = None
    # 种子标题
    subject: Optional[str] = None
    # 以及类目
    cate_level1: Optional[CateLevel1] = None
    # 站点类目id
    cate_id: Optional[str] = None
    # 种子详情页地址
    details_url: Optional[str] = None
    # 种子下载链接
    download_url: Optional[str] = None
    # 种子关联的imdbid
    imdb_id: Optional[str] = None
    # 种子发布时间
    publish_date: Optional[datetime] = None
    # 种子大小，转化为mb尺寸
    size_mb: Optional[float] = None
    # 做种人数
    upload_count: Optional[int] = None
    # 下载中人数
    downloading_count: Optional[int] = None
    # 下载完成人数
    download_count: Optional[int] = None
    # 免费截止时间
    free_deadline: Optional[datetime] = None
    # 下载折扣，1为不免费
    download_volume_factor: Optional[float] = None
    # 做种上传系数，1为正常
    upload_volume_factor: Optional[int] = None
    minimum_ratio: float = 0
    minimum_seed_time: int = 0
    # 封面链接
    poster_url: Optional[str] = None


@dataclass
class TorrentDetail:
    site_id: Optional[str] = None
    name: Optional[str] = None
    subject: Optional[str] = None
    download_url: Optional[str] = None
    filename: Optional[str] = None
    intro: Optional[str] = None
    publish_date: Optional[datetime] = None
