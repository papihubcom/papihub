import datetime
import os

from sqlalchemy import create_engine, Column, DateTime, String, Integer, Text, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

db_path = os.path.join(os.environ.get('WORKDIR', os.path.dirname(os.path.abspath(__file__))), 'db')
if not os.path.exists(db_path):
    os.makedirs(db_path)
engine = create_engine(
    f'sqlite:////{db_path}/main.db?check_same_thread=False&timeout=60'
)
Base = declarative_base()


def create_all():
    Base.metadata.create_all(engine)


class BaseDBModel(Base):
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
