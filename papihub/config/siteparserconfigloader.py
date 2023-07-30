import os
from typing import List, Dict

import yaml

from papihub.config.types import TorrentSiteParserConfig, ParserConfig
from papihub.exceptions import ParserConfigErrorException


class SiteParserConfigLoader:
    """
    站点适配文件加载器
    """

    def __init__(self, conf_path: str):
        if not conf_path or not os.path.exists(conf_path):
            raise FileNotFoundError(conf_path, f'站点适配文件路径不存在：{conf_path}')
        self.conf_path = conf_path

    def load(self) -> Dict[str, ParserConfig]:
        if not self.conf_path:
            return {}
        parse_configs = {}
        for path, dir_list, file_list in os.walk(self.conf_path):
            for file_name in file_list:
                if os.path.splitext(file_name)[1] != '.yml':
                    continue
                filepath = os.path.join(self.conf_path, file_name)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        parser_config_dict = yaml.safe_load(''.join(lines))
                        config_type: str = parser_config_dict.get('config_type')
                        if config_type == 'torrent_site':
                            parse_configs[parser_config_dict.get('site_id')] = TorrentSiteParserConfig(
                                **parser_config_dict)
                except Exception as e:
                    raise ParserConfigErrorException(filepath,
                                                     f'站点适配文件错误，请检查文件是否标准yml文件，没有掺杂无效信息：{filepath}',
                                                     e)
        return parse_configs
