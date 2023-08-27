from papihub.signals import site_init_signal


@site_init_signal.connect
def on_site_init(site_id: str):
    print(site_id)
    # todo 初始化站点，比如登录，获取cookie等。检查有效性后，更新站点状态为正常
