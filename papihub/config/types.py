from typing import Optional, List, Dict
from dataclasses import dataclass


@dataclass
class ParserConfig:
    config_type: Optional[str] = None
    # 站点编号
    site_id: Optional[str] = None
    # 站点名称
    site_name: Optional[str] = None
    # 站点类型
    site_type: Optional[str] = None
    # 站点域名
    domain: Optional[str] = None
    # 站点编码
    encoding: Optional[str] = None


@dataclass
class TorrentSiteParserConfig(ParserConfig):
    login: Optional[Dict] = None
    # 站点类目映射
    category_mappings: Optional[List[Dict]] = None
    category_id_mapping: Optional[List[Dict]] = None
    # 用户信息解析配置
    user: Optional[Dict] = None
    # 搜索解析配置
    search: Optional[Dict] = None
    # 独立的种子列表页解析配置
    get_list: Optional[Dict] = None
    # 标准种子解析配置
    torrents: Optional[Dict] = None
    get_detail: Optional[Dict] = None
