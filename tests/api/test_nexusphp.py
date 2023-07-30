import asyncio

from papihub.api.sites.nexusphp import NexusPhp
from papihub.api.types import CateLevel1
from tests.config.test_siteparserconfigload import test_load_parser

parsers = test_load_parser()


def test_search():
    api = NexusPhp(parsers.get('mteam'))
    asyncio.run(api.auth('xxx', 'xxx'))
    torrents = asyncio.run(api.search(keyword='潜行者', cate_level1_list=[CateLevel1.TV]))
