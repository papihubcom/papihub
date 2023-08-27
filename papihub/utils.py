import datetime
import decimal
import json
from enum import Enum
from typing import _GenericAlias, List, Union, Dict

import emoji


def _list_value(value):
    if isinstance(value, str):
        if value[0] in ['{', '[']:
            return json.loads(value)
        else:
            return value.split(',')
    else:
        return list(value)


def _dict_value(value):
    if isinstance(value, str):
        return json.loads(value)
    else:
        return value


def parse_field_value(field_value):
    if isinstance(field_value, decimal.Decimal):  # Decimal -> float
        field_value = round(float(field_value), 2)
    elif isinstance(field_value, datetime.datetime):  # datetime -> str
        field_value = str(field_value)
    elif isinstance(field_value, list):
        field_value = [parse_field_value(i) for i in field_value]
    if hasattr(field_value, 'to_json'):
        field_value = field_value.to_json()
    elif isinstance(field_value, Enum):
        field_value = field_value.name
    elif isinstance(field_value, Dict):
        val = {}
        for key_ in field_value:
            val[key_] = parse_field_value(field_value[key_])
        field_value = val
    return field_value


def parse_value(func, value, default_value=None):
    if value is not None:
        if func == bool:
            if value in (1, True, "1", "true"):
                return True
            elif value in (0, False, "0", "false"):
                return False
            else:
                raise ValueError(value)

        elif func in (int, float):
            try:
                if isinstance(value, str):
                    value = value.replace(',', '')
                return func(value)
            except ValueError:
                return float('nan')
        elif func == datetime.datetime:
            if isinstance(value, datetime.datetime):
                return value
            elif isinstance(value, str):
                if value:
                    return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                else:
                    return None
            else:
                return None
        elif func in [Dict, dict]:
            return _dict_value(value)
        elif func in [List, list]:
            return _list_value(value)
        elif isinstance(func, _GenericAlias):
            if func.__origin__ in [List, list]:
                list_ = _list_value(value)
                res = []
                for x in list_:
                    res.append(parse_value(func.__args__[0], x))
                return res
            elif func.__origin__ == Union:
                return parse_value(func.__args__[0], value)
        return func(value)
    else:
        return default_value


def trim_emoji(text):
    """
    去掉字符串中的emoji表情
    :param text:
    :return:
    """
    return emoji.demojize(text)


def trans_size_str_to_mb(size: str):
    """
    把一个字符串格式的文件尺寸单位，转换成MB单位的标准数字
    :param size:
    :return:
    """
    if not size:
        return 0.0
    s = None
    u = None
    if size.find(' ') != -1:
        arr = size.split(' ')
        s = arr[0]
        u = arr[1]
    else:
        if size.endswith('GB'):
            s = size[0:-2]
            u = 'GB'
        elif size.endswith('GiB'):
            s = size[0:-3]
            u = 'GB'
        elif size.endswith('MB'):
            s = size[0:-2]
            u = 'MB'
        elif size.endswith('MiB'):
            s = size[0:-3]
            u = 'MB'
        elif size.endswith('KB'):
            s = size[0:-2]
            u = 'KB'
        elif size.endswith('KiB'):
            s = size[0:-3]
            u = 'KB'
        elif size.endswith('TB'):
            s = size[0:-2]
            u = 'TB'
        elif size.endswith('TiB'):
            s = size[0:-3]
            u = 'TB'
        elif size.endswith('PB'):
            s = size[0:-2]
            u = 'PB'
        elif size.endswith('PiB'):
            s = size[0:-3]
            u = 'PB'
    if not s:
        return 0.0
    if s.find(',') != -1:
        s = s.replace(',', '')
    return trans_unit_to_mb(float(s), u)


def trans_unit_to_mb(size: float, unit: str) -> float:
    """
    按文件大小尺寸规格，转换成MB单位的数字
    :param size:
    :param unit:
    :return:
    """
    if unit == 'GB' or unit == 'GiB':
        return round(size * 1024, 2)
    elif unit == 'MB' or unit == 'MiB':
        return round(size, 2)
    elif unit == 'KB' or unit == 'KiB':
        return round(size / 1024, 2)
    elif unit == 'TB' or unit == 'TiB':
        return round(size * 1024 * 1024, 2)
    elif unit == 'PB' or unit == 'PiB':
        return round(size * 1024 * 1024 * 1024, 2)
    else:
        return size
