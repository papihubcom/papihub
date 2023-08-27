import datetime
import logging
import re
import urllib

from pyquery import PyQuery

from papihub.exceptions import ParserFieldException

_LOGGER = logging.getLogger(__name__)


def filter_querystring(value, args):
    if value.startswith('?'):
        value = value[1:]
    elif value.find('?') != -1:
        value = value.split('?')[1]
    qs = urllib.parse.parse_qs(value)
    value = qs.get(args)
    if value:
        value = value[0]
    return value


def filter_split(value, args):
    arr = value.split(args[0])
    if args[1] < len(arr):
        return arr[args[1]]
    return None


def filter_re_search(value, args):
    result = re.search(args[0], value)
    if result:
        if args[1] <= len(result.groups()):
            return result.group(args[1])
        else:
            return
    return


def filter_parse_date_elapsed(value, args) -> datetime:
    t = re.match(r'(?:(\d+)日)?(?:(\d+)[時时])?(?:(\d+)分)?', value)
    if not t:
        return None
    now = datetime.datetime.now()
    if t.group(1):
        now = now + datetime.timedelta(days=int(t.group(1)))
    if t.group(2):
        now = now + datetime.timedelta(hours=int(t.group(2)))
    if t.group(3):
        now = now + datetime.timedelta(minutes=int(t.group(3)))
    return now


def filter_parse_date_elapsed_en(value, args):
    if not value:
        return
    value = str(value).strip()
    t = re.match(r'([\d\.]+)\s(seconds|minutes|hours|days|weeks|years)\sago', value)
    if not t:
        return
    now = datetime.datetime.now()
    num = t.group(1)
    unit = t.group(2)
    if unit == 'seconds':
        now = now + datetime.timedelta(seconds=float(num))
    elif unit == 'minutes':
        now = now + datetime.timedelta(minutes=float(num))
    elif unit == 'hours':
        now = now + datetime.timedelta(hours=float(num))
    elif unit == 'days':
        now = now + datetime.timedelta(days=float(num))
    elif unit == 'weeks':
        now = now + datetime.timedelta(weeks=float(num))
    elif unit == 'years':
        now = now + datetime.timedelta(days=float(num) * 365)
    return now


def filter_regexp(value, args):
    return re.sub(args, '', value)


def filter_dateparse(value, args):
    if not value:
        return datetime.datetime.now()
    value = str(value)
    if isinstance(args, list):
        args = args
    else:
        args = [str(args)]
    for f in args:
        try:
            try:
                return datetime.datetime.strptime(value, f)
            except ValueError as e:
                if value.startswith('今天'):
                    value = value.replace('今天', datetime.datetime.now().strftime('%Y-%m-%d'))
                    return filter_dateparse(value, args)
                elif value.startswith('昨天'):
                    value = value.replace('昨天',
                                          (datetime.datetime.now() - datetime.timedelta(days=-1)).strftime('%Y-%m-%d'))
                    return filter_dateparse(value, args)
                raise e
        except ValueError as e:
            continue
    return


filter_handler = {
    'lstrip': lambda val, args: str(val).lstrip(str(args[0])),
    'rstrip': lambda val, args: str(val).rstrip(str(args[0])),
    'replace': lambda val, args: val.replace(args[0], args[1]) if val else None,
    'append': lambda val, args: val + args,
    'prepend': lambda val, args: args + val,
    'tolower': lambda val, args: val.lower(),
    'toupper': lambda val, args: val.upper(),
    'split': filter_split,
    'dateparse': filter_dateparse,
    'querystring': filter_querystring,
    're_search': filter_re_search,
    'date_elapsed_parse': filter_parse_date_elapsed,
    'date_en_elapsed_parse': filter_parse_date_elapsed_en,
    'regexp': filter_regexp
}


class HtmlParser:
    @staticmethod
    def _select_value(tag: PyQuery, rule):
        val = None
        if tag:
            if 'attribute' in rule:
                attr = tag.attr(rule['attribute'])
                if attr:
                    if isinstance(attr, list):
                        val = attr[0]
                    else:
                        val = attr
            elif 'method' in rule:
                if rule['method'] == 'next_sibling' and tag:
                    val = tag[0].tail
            elif 'remove' in rule:
                remove_tag_name = rule['remove'].split(',')
                for rt in remove_tag_name:
                    tag.remove(rt)
                val = tag.text()
            elif 'contents' in rule:
                idx = rule['contents']
                e = tag.eq(0).contents()[idx]
                if hasattr(e, 'text'):
                    val = e.text
                else:
                    val = str(e)
            else:
                val = tag.text()
        if val:
            val = val.strip()
        return val

    @staticmethod
    def _case_value(r: PyQuery, case):
        val = None
        for ck in case:
            if ck == '*':
                val = case[ck]
                break
            if r(ck):
                val = case[ck]
                break
        return val

    @staticmethod
    def _filter_value(value, filters):
        if not value:
            return value
        for f in filters:
            if f['name'] in filter_handler:
                value = filter_handler[f['name']](value, f.get('args'))
        return value

    @staticmethod
    def parse_item_fields(item_tag: PyQuery, item_rule, context=None):
        if not item_tag:
            return {}
        self = HtmlParser
        values = {}
        for key in item_rule:
            rule = item_rule[key]
            val = None
            try:
                if 'text' in rule:
                    if '_template' in rule:
                        tmpl = rule['_template']
                        ctx = {'fields': values, 'now': datetime.datetime.now()}
                        if context:
                            ctx.update(context)
                        val = tmpl.render(ctx)
                    else:
                        val = rule.get('text')
                elif 'selector' in rule:
                    val = self._select_value(item_tag(rule['selector']), rule)
                elif 'selectors' in rule:
                    tag_list = item_tag(rule['selectors'])
                    if rule.get('index'):
                        if tag_list and rule['index'] < tag_list.length:
                            tag = tag_list.eq(rule['index'])
                            val = self._select_value(tag, rule)
                    else:
                        val = []
                        for i in range(tag_list.length):
                            val.append(self._select_value(tag_list.eq(i), rule))
                elif 'case' in rule:
                    val = self._case_value(item_tag, rule['case'])
                if 'filters' in rule:
                    val = self._filter_value(val, rule['filters'])
                if not val and 'default_value' in rule:
                    if '_default_value_template' in rule:
                        tmpl = rule['_default_value_template']
                        ctx = {'fields': values, 'now': datetime.datetime.now(), 'max_time': datetime.datetime.max}
                        if context:
                            ctx.update(context)
                        val = tmpl.render(ctx)
                    else:
                        val = rule['default_value']
                    if val and 'default_value_format' in rule:
                        val = datetime.datetime.strptime(val, rule['default_value_format'])
            except Exception as e:
                raise ParserFieldException(key, e)
            values[key] = val
        return values
