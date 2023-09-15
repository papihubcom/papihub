"""
与数据库有关的操作类
"""
import datetime
import os

from dataclasses_json import dataclass_json
from sqlalchemy import create_engine, Column, DateTime, String, Integer, Text, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from papihub import utils

# WORKDIR环境变量文件夹内的db目录，为数据库文件存放目录
db_path = os.path.join(os.environ.get('WORKDIR', os.path.dirname(os.path.abspath(__file__))), 'db')
if not os.path.exists(db_path):
    os.makedirs(db_path)
engine = create_engine(
    f'sqlite:////{db_path}/main.db?check_same_thread=False&timeout=60'
)
Base = declarative_base()


def create_all():
    """
    自动初始化数据库引擎和ORM框架
    会自动生成模型定义的结构为数据表
    :return:
    """
    Base.metadata.create_all(engine)


class BaseDBModel(Base):
    """
    数据表基类，每张表的模型类继承此类
    """
    __abstract__ = True
    __table_args__ = {'extend_existing': True}
    gmt_create = Column(DateTime, nullable=False, default=datetime.datetime.now)
    gmt_modified = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def get_columns(self):
        """
        返回所有字段对象
        :return:
        """
        return self.__table__.columns

    @classmethod
    def query(cls):
        session = Session(bind=engine)
        return session.query(cls)

    def get_fields(self):
        """
        返回所有字段
        :return:
        """
        return self.__dict__

    def save(self):
        """
        新增
        :return:
        """
        session = Session(bind=engine)
        try:
            session.add(self)
            session.commit()
        except BaseException as e:
            session.rollback()
            raise

    def update(self):
        """
        新增
        :return:
        """
        session = Session(bind=engine)
        try:
            self.gmt_modified = datetime.datetime.now()
            session.merge(self)
            session.commit()
        except:
            session.rollback()
            raise

    @staticmethod
    def save_all(model_list):
        """
        批量新增
        :param model_list:
        :return:
        """
        session = Session(bind=engine)
        try:
            session.add_all(model_list)
            session.commit()
        except:
            session.rollback()
            raise

    def delete(self):
        session = Session(bind=engine)
        try:
            session.commit()
        except:
            session.rollback()
            raise

    def to_dict(self, hidden_fields=None):
        """
        Json序列化
        :param hidden_fields: 覆盖类属性 hidden_fields
        :return:
        """
        model_json = {}
        if not hidden_fields:
            hidden_fields = self.__hidden_fields__
        if not hidden_fields:
            hidden_fields = []
        for column in self.__dict__:
            if column in hidden_fields:
                continue
            if hasattr(self, column):
                model_json[column] = utils.parse_field_value(getattr(self, column))
        if '_sa_instance_state' in model_json:
            del model_json['_sa_instance_state']
        return model_json
