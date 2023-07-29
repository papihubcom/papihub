import abc


class Auth(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def auth_with_cookies(self, cookies_str: str):
        pass

    @abc.abstractmethod
    async def auth(self, username: str, password: str):
        pass
