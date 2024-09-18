from math import ceil
from sqlalchemy import create_engine, Column, Integer, DateTime, func
from sqlalchemy.engine import Row
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from config.env import DataBaseConfig
from utils.log_util import logger

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@" \
                          f"{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=DataBaseConfig.db_echo,
    max_overflow=DataBaseConfig.db_max_overflow,
    pool_size=DataBaseConfig.db_pool_size,
    pool_recycle=DataBaseConfig.db_pool_recycle,
    pool_timeout=DataBaseConfig.db_pool_timeout
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    created_time = Column(DateTime(timezone=True), default=func.now(), nullable=False, comment='创建时间')
    update_time = Column(DateTime(timezone=True), default=func.now(), nullable=False, onupdate=func.now(),
                         comment='更新时间')

    def to_dict(self, db=None):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        model_dict['created_time'] = model_dict['created_time'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(
            model_dict['created_time'], object) else model_dict['created_time']
        model_dict['update_time'] = model_dict['update_time'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(
            model_dict['update_time'], object) else model_dict['update_time']
        if model_dict.get('task_start_time'):
            utc_datetime = model_dict.get('task_start_time')
            naive_datetime = utc_datetime.replace(tzinfo=None) if utc_datetime.tzinfo else utc_datetime
            model_dict['task_start_time'] = naive_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return model_dict

    Base.to_dict = to_dict

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, Column):
                attr_value.nullable = False


# 分页器
class MyPagination:
    def __init__(self, query, page: int = 1, page_size: int = 10):
        """
        初始化分页参数
        :param query: 查询对象
        :param page_size: 一页多少内容
        :param page: 第几页 1起
        """
        self.query = query
        self.page = page
        self.page_size = page_size

    @property
    def items(self):
        """
        分页后数据
        :return: [model row / Model]
        """
        # if self.page > self.pages:
        #     return []
        offset_num = (self.page - 1) * self.page_size  # 计算偏移量
        return self.query.limit(self.page_size).offset(offset_num).all()

    @staticmethod
    def _to_dict(piece):
        res = {}
        if isinstance(piece, Row):
            for key, value in piece._mapping.items():
                res.update(value.to_dict()) if isinstance(value, Base) else res.update({key: value})
            return res
        return piece.to_dict()

    @property
    def data(self):
        return [self._to_dict(piece) for piece in self.items]

    @property
    def counts(self):
        """
        总数据量
        :return: int
        """
        return self.query.count()

    @property
    def pages(self):
        """
        总页数
        :return: int
        """
        return ceil(self.counts / self.page_size)


def get_db_pro():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    current_db = SessionLocal()
    try:
        yield current_db
    finally:
        current_db.close()


async def init_create_table():
    """
    应用启动时初始化数据库连接
    :return:
    """
    logger.log_info("初始化数据库连接...")
    Base.metadata.create_all(bind=engine)
    logger.log_info("数据库连接成功")


get_db = get_db_pro
