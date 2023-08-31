import abc


class Auth(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def auth_with_cookies(self, cookies_str: str):
        pass

    @abc.abstractmethod
    def auth(self, username: str, password: str):
        pass

    @abc.abstractmethod
    def test_login(self) -> bool:
        pass
