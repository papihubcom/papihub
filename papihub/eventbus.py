"""
程序事件管理类
程序内产生的所有事件，都统一在此处描述
"""
from event_bus import EventBus

# 全局默认的事件处理器
bus = EventBus()
# 站点初始化事件
EVENT_SITE_INIT = 'site:init'
