"""
常量信息类
"""
from papihub.api.types import CateLevel1

# 默认所有种子搜索的一级分类
ALL_CATE_LEVEL1 = [CateLevel1.Movie,
                   CateLevel1.TV,
                   CateLevel1.Documentary,
                   CateLevel1.Anime,
                   CateLevel1.Music,
                   CateLevel1.AV,
                   CateLevel1.Game,
                   CateLevel1.Other]

# 全局http请求的默认头
BASE_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
