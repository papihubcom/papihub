from blinker import signal

"""
应用中的异步事件
"""
site_init_signal = signal('site_init', doc='站点初始化')
