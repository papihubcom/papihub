from http.cookies import SimpleCookie
from typing import Optional, List, Dict

import httpx
from httpx import Timeout
from jinja2 import Template
from pyquery import PyQuery

from papihub import utils
from papihub.api.auth import Auth
from papihub.api.torrentsite import TorrentSite
from papihub.api.types import TorrentDetail, Torrent, TorrentSiteUser, ApiOptions, CateLevel1
from papihub.config.types import TorrentSiteParserConfig
from papihub.constants import BASE_HEADERS
from papihub.exceptions import NotAuthenticatedException

DEFAULT_LOGIN_PATH = '/takelogin.php'


class NexusPhp(TorrentSite, Auth):
    """
    NexusPHP站点架构解析器，此实现类有以下特点
    1、此类带有站点登录功能
    2、此类遵循NexusPHP站点分类设计，搜索时会自动找到正确的搜索分类进行搜索
    """
    auth_cookies: Optional[Dict[str, str]] = None
    auth_headers: Optional[Dict[str, str]] = None
    _search_paths: List
    _search_query: Dict

    def __init__(self, parser_config: TorrentSiteParserConfig, options: Optional[ApiOptions] = None):
        self.parser_config = parser_config
        if not options:
            options = ApiOptions()
            options.request_timeout = 20
        self.options = options
        self._init()

    def _init(self):
        """
        初始化站点配置信息
        :return:
        """
        for c in self.parser_config.category_mappings:
            # id to string
            c['id'] = str(c['id'])
        self.parser_config.domain = self.parser_config.domain.rstrip('/')
        self._init_jinja_template(self.parser_config.torrents.get('fields'))
        if self.parser_config.get_list:
            self._init_jinja_template(self.parser_config.get_list.get('fields'))
        self._search_paths = self._init_search_paths(self.parser_config.search.get('paths'),
                                                     self.parser_config.category_mappings)
        self._search_query = self._init_search_query(self.parser_config.search.get('query'))
        self.auth_headers = BASE_HEADERS.copy()
        self.auth_headers['Referer'] = self.parser_config.domain
        if self.options.user_agent:
            self.auth_headers['User-Agent'] = self.options.user_agent

    @staticmethod
    def _init_search_paths(paths_config, category_mappings):
        """
        根据类目的配置，加载搜索配置，把搜索路径及可用的类目组合，方便搜索时查找
        :param paths_config:
        :param category_mappings:
        :return:
        """
        paths = []
        for p in paths_config:
            obj: dict = dict()
            obj['path'] = p.get('path')
            cate_ids_config = p.get('categories')
            search_cate_ids = []
            if cate_ids_config:
                # 如果可用id第一个字符为!，则说明是排除设置模式
                if cate_ids_config[0] == '!':
                    for c in category_mappings:
                        if (int(c['id']) if c['id'] else 0) not in cate_ids_config:
                            search_cate_ids.append(str(c['id']))
                else:
                    search_cate_ids = [str(c) for c in cate_ids_config]
            else:
                search_cate_ids = [str(c['id']) for c in category_mappings]
            obj['categories'] = search_cate_ids
            if p.get('method'):
                obj['method'] = p.get('method')
            else:
                obj['method'] = 'get'
            paths.append(obj)
        return paths

    @staticmethod
    def _init_search_query(query_config):
        query_tmpl = {}
        for key in query_config:
            val = query_config[key]
            if isinstance(val, str) and val.find('{') != -1:
                query_tmpl[key] = Template(val)
            else:
                query_tmpl[key] = val
        return query_tmpl

    @staticmethod
    def _init_jinja_template(fields):
        """
        把fields中使用到的jinja2模版提前编译好
        :param fields:
        :return:
        """
        if not fields:
            return
        if fields:
            for key in fields:
                rule = fields[key]
                if 'text' in rule:
                    if isinstance(rule['text'], str) and rule['text'].find('{') != -1:
                        rule['_template'] = Template(rule['text'])
                if 'default_value' in rule:
                    if isinstance(rule['default_value'], str) and rule['default_value'].find('{') != -1:
                        rule['_default_value_template'] = Template(rule['default_value'])

    def _set_auth_cookies(self, cookie_str: str):
        if not cookie_str:
            return
        cookie = SimpleCookie(cookie_str)
        cookies = {}
        for key, morsel in cookie.items():
            cookies[key] = morsel.value
        self.auth_cookies = cookies

    def _get_cate_level2_ids(self, cate_level1_list: Optional[List[CateLevel1]] = None):
        """
        通过一级大分类，去找到配置好的站点二级小分类，真正搜索时，搜站点二级小分类的编号
        :param cate_level1_list:
        :return:
        """
        if not cate_level1_list:
            ids = []
            # 默认不查成人
            for c in self.parser_config.category_mappings:
                if c['cate_level1'] == CateLevel1.AV.name:
                    continue
                ids.append(c['id'])
            return ids
        cate_level1_str_arr = [i.name for i in cate_level1_list]
        cate2_ids = []
        # 找到一级分类下所有的二级分类编号
        for c in self.parser_config.category_mappings:
            if c.get('cate_level1') in cate_level1_str_arr or c.get('cate_level1') == '*':
                cate2_ids.append(c.get('id'))
        return cate2_ids

    def _build_search_path(self, cate_level1_list: Optional[List[CateLevel1]]) -> List[Dict]:
        if not cate_level1_list:
            cate_level1_list = [x for x in CateLevel1]
        input_cate2_ids = set(self._get_cate_level2_ids(cate_level1_list))
        paths = []
        # 根据传入一级分类数据，查找真正要执行的搜索path，一级对应分类
        for p in self._search_paths:
            cpath = p.copy()
            cate_in = list(set(cpath['categories']).intersection(input_cate2_ids))
            if not cate_in:
                continue
            del cpath['categories']
            if len(cate_in) == len(self.parser_config.category_mappings):
                # 如果等于全部，不需要传分类
                cpath['query_cates'] = []
            else:
                cpath['query_cates'] = cate_in
            paths.append(cpath)
        return paths

    def _trans_search_cate_id(self, ids):
        if not ids:
            return ids
        id_mapping = self.parser_config.category_id_mapping
        if not id_mapping:
            return ids
        new_ids = []
        for _id in ids:
            for mid in id_mapping:
                if mid.get('id') == _id:
                    if isinstance(mid.get('mapping'), list):
                        new_ids += mid.get('mapping')
                    else:
                        new_ids.append(mid.get('mapping'))
        new_ids = list(filter(None, new_ids))
        if not new_ids:
            return ids
        return new_ids

    def _render_querystring(self, query_context: Dict):
        qs = ''
        for key in self._search_query:
            val = self._search_query[key]
            if isinstance(val, Template):
                val = val.render({'query': query_context})
            if key == '$raw' and val is not None and val != '':
                qs += val
            elif val is not None and val != '':
                qs += f'{key}={val}&'
        if qs:
            qs = qs.rstrip('&')
        return qs

    def _get_response_text(self, response):
        if not response:
            return
        c = response.content
        if not c:
            return
        s = str(response.content, self.parser_config.encoding)
        return utils.trim_emoji(s)

    @staticmethod
    def _is_login(response) -> bool:
        if not response:
            return False
        if response.url.path.startswith('/login.php'):
            return False
        return True

    async def auth_with_cookies(self, cookies_str: str):
        self._set_auth_cookies(cookies_str)

    async def auth(self, username: str, password: str):
        async with httpx.AsyncClient(
                headers=self.auth_headers,
                cookies=self.auth_cookies,
                timeout=Timeout(self.options.request_timeout) if self.options else None,
                proxies=self.options.proxies,
                follow_redirects=True,
                verify=False
        ) as client:
            if self.parser_config.login and self.parser_config.login.get('path'):
                login_path = f'{self.parser_config.domain}{self.parser_config.login.get("path")}'
            else:
                login_path = f'{self.parser_config.domain}{DEFAULT_LOGIN_PATH}'
            login_method = self.parser_config.login.get('method') if self.parser_config.login else 'post'
            if login_method == 'get':
                res = await client.get(f'{login_path}?username={username}&password={password}')
            else:
                res = await client.post(login_path, data={
                    'username': username,
                    'password': password
                })
            if res.url.path.startswith('/index') and res.history:
                cookies_str = res.history[-1].headers.get('Set-Cookie')
                self._set_auth_cookies(cookies_str)
                return cookies_str
            else:
                raise NotAuthenticatedException(self.parser_config.site_id, self.parser_config.site_name,
                                                f'{self.parser_config.site_name}登录失败，用户名或密码错误')

    async def list(self, timeout=None, cate_level1_list=None) -> List[Torrent]:
        pass

    async def get_user(self, refresh=False) -> Optional[TorrentSiteUser]:
        pass

    async def search(self, keyword: Optional[str] = None,
                     imdb_id: Optional[str] = None,
                     cate_level1_list: Optional[List] = None,
                     free: Optional[bool] = False,
                     page: Optional[int] = None,
                     timeout: Optional[int] = None) -> List[Torrent]:
        if not self._search_paths:
            return []
        paths = self._build_search_path(cate_level1_list)
        if not paths:
            # 配置文件的分类设置有问题或者真的不存在所需查询分类
            return []
        # 构造查询参数的上下文，供配置渲染真实querystring
        query_context = {}
        if keyword:
            query_context['keyword'] = keyword
        if imdb_id:
            query_context['imdb_id'] = imdb_id
        if free:
            query_context['free'] = free
        else:
            query_context['cates'] = []
        if page:
            query_context['page'] = page
        search_result: List[Torrent] = []
        if not timeout:
            timeout = self.options.request_timeout
        for i, p in enumerate(paths):
            if p.get('query_cates'):
                query_context['cates'] = self._trans_search_cate_id(p.get('query_cates'))
            uri = p.get('path')
            qs = self._render_querystring(query_context)
            async with httpx.AsyncClient(
                    headers=self.auth_headers,
                    cookies=self.auth_cookies,
                    timeout=Timeout(timeout),
                    proxies=self.options.proxies,
                    follow_redirects=True,
                    verify=False
            ) as client:
                if p.get('method') == 'get':
                    url = f'{self.parser_config.domain}/{uri}?{qs}'
                    res = await client.get(url)
                else:
                    url = f'{self.parser_config.domain}/{uri}'
                    res = await client.post(url, data=qs)
                if not self._is_login(res):
                    raise NotAuthenticatedException(self.parser_config.site_id, self.parser_config.site_name,
                                                    f'{self.parser_config.site_name}未授权，无法访问')
                text = self._get_response_text(res)
                if not text:
                    continue
                torrents = []
                # todo parse torrent
                if torrents:
                    search_result += torrents
        return search_result

    async def download_torrent(self, url, filepath):
        pass

    async def get_detail(self, url) -> Optional[TorrentDetail]:
        pass
