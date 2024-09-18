import io
import os
from contextlib import contextmanager
from io import StringIO
from dotenv.main import DotEnv
from pydantic import BaseSettings, Field
from functools import lru_cache
from dotenv import load_dotenv


def my_get_stream(self):
    """重写python-dotenv读取文件的方法，使用utf-8，支持读取包含中文的.env配置文件"""
    if isinstance(self.dotenv_path, StringIO):
        yield self.dotenv_path
    elif os.path.isfile(self.dotenv_path):
        with io.open(self.dotenv_path, encoding='utf-8') as stream:
            yield stream
    else:
        if self.verbose:
            print("File doesn't exist %s", self.dotenv_path)
        yield StringIO('')


DotEnv._get_stream = contextmanager(my_get_stream)


class AppSettings(BaseSettings):
    """
    应用配置
    """
    app_env: str = Field(None, env="APP_ENV")
    app_name: str = Field(None, env="APP_NAME")
    app_root_path: str = Field(None, env="APP_ROOT_PATH")
    app_host: str = Field(None, env="APP_HOST")
    app_port: int = Field(None, env="APP_PORT")
    app_version: str = Field(None, env="APP_VERSION")
    app_reload: bool = Field(None, env="APP_RELOAD")
    app_ip_location_query: bool = Field(None, env="APP_IP_LOCATION_QUERY")
    app_same_time_login: bool = Field(None, env="APP_SAME_TIME_LOGIN")


class JwtSettings(BaseSettings):
    """
    Jwt配置
    """
    jwt_secret_key: str = Field(None, env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(None, env="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(None, env="JWT_EXPIRE_MINUTES")
    jwt_redis_expire_minutes: int = Field(None, env="JWT_REDIS_EXPIRE_MINUTES")


class DataBaseSettings(BaseSettings):
    """
    数据库配置
    """
    db_host: str = Field(None, env="DB_HOST")
    db_port: str = Field(None, env="DB_PORT")
    db_username: str = Field(None, env="DB_USERNAME")
    db_password: str = Field(None, env="DB_PASSWORD")
    db_database: str = Field(None, env="DB_DATABASE")
    db_echo: bool = Field(None, env="DB_ECHO")
    db_max_overflow: int = Field(None, env="DB_MAX_OVERFLOW")
    db_pool_size: int = Field(None, env="DB_POOL_SIZE")
    db_pool_recycle: int = Field(None, env="DB_POOL_RECYCLE")
    db_pool_timeout: int = Field(None, env="DB_POOL_TIMEOUT")


class RedisSettings(BaseSettings):
    """
    Redis配置
    """
    redis_host: str = Field(None, env="REDIS_HOST")
    redis_port: int = Field(None, env="REDIS_PORT")
    redis_username: str = Field(None, env="REDIS_USERNAME")
    redis_password: str = Field(None, env="REDIS_PASSWORD")
    redis_database: int = Field(None, env="REDIS_DATABASE")
    celery_beat_db: int = Field(None, env="CELERY_BEAT_DB")


class RabbitMQSettings(BaseSettings):
    rabbitmq_host: str = Field(None, env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(None, env="RABBITMQ_PORT")
    rabbitmq_username: str = Field(None, env="RABBITMQ_USERNAME")
    rabbitmq_password: str = Field(None, env="RABBITMQ_PASSWORD")
    rabbitmq_virtual_host: str = Field(None, env="RABBITMQ_VIRTUAL_HOST")


class CachePathConfig:
    """
    缓存目录配置
    """
    PATH = os.path.join(os.path.abspath(os.getcwd()), 'caches')
    PATHSTR = 'caches'


class RedisInitKeyConfig:
    """
    系统内置Redis键名
    """
    ACCESS_TOKEN = {'key': 'access_token', 'remark': '登录令牌信息'}
    SYS_DICT = {'key': 'sys_dict', 'remark': '数据字典'}
    SYS_CONFIG = {'key': 'sys_config', 'remark': '配置信息'}
    CAPTCHA_CODES = {'key': 'captcha_codes', 'remark': '图片验证码'}
    ACCOUNT_LOCK = {'key': 'account_lock', 'remark': '用户锁定'}
    PASSWORD_ERROR_COUNT = {'key': 'password_error_count', 'remark': '密码错误次数'}
    SMS_CODE = {'key': 'sms_code', 'remark': '短信验证码'}


class GetConfig:
    """
    获取配置
    """

    def __init__(self):
        self.parse_env()

    @lru_cache()
    def get_app_config(self):
        """
        获取应用配置
        """
        # 实例化应用配置模型
        return AppSettings()

    @lru_cache()
    def get_jwt_config(self):
        """
        获取Jwt配置
        """
        # 实例化Jwt配置模型
        return JwtSettings()

    @lru_cache()
    def get_database_config(self):
        """
        获取数据库配置
        """
        # 实例化数据库配置模型
        return DataBaseSettings()

    @lru_cache()
    def get_redis_config(self):
        """
        获取Redis配置
        """
        # 实例化Redis配置模型
        return RedisSettings()

    @staticmethod
    def parse_env():
        # 运行环境未指定时默认加载.env
        env_file = '.env'
        # 加载配置
        load_dotenv(env_file)


# 实例化获取配置类
get_config = GetConfig()
# 应用配置
AppConfig = get_config.get_app_config()
# Jwt配置
JwtConfig = get_config.get_jwt_config()
# 数据库配置
DataBaseConfig = get_config.get_database_config()
# Redis配置
RedisConfig = get_config.get_redis_config()
