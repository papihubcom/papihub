from dataclasses import dataclass

from papihub.databases import *

from papihub.databases import BaseDBModel


class UserModel(BaseDBModel):
    """
    存储站点用的一些Cookie
    """
    __tablename__ = 'user'
    __hidden_fields__ = ['password']
    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    nickname = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False)
    password = Column(String(256), nullable=False)

    @staticmethod
    def get_by_username(username: str) -> "UserModel":
        """
        根据用户名获取用户信息，只返回首条结果
        :param username:
        :return:
        """
        return UserModel.query().filter(UserModel.username == username).first()
