import abc


class Auth(metaclass=abc.ABCMeta):
    """
    站点认证信息类
    不需要认证的站点，无需实现此接口
    """

    @abc.abstractmethod
    def auth_with_cookies(self, cookies_str: str):
        """
        通过Cookies完成认证
        :param cookies_str: Cookies字符串
        :return:
        """
        pass

    @abc.abstractmethod
    def auth(self, username: str, password: str) -> str:
        """
        通过用户名密码完成认证
        :param username: 用户名
        :param password: 密码
        :return: 返回授权后的cookies字符串
        """
        pass

    @abc.abstractmethod
    def test_login(self) -> bool:
        """
        测试登录
        :return:
        """
        pass
