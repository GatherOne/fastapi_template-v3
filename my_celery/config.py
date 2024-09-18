# -*- coding: utf-8 -*-
from kombu import Exchange, Queue
from config.env import RabbitMQSettings, RedisSettings, AppConfig
from config.database import SQLALCHEMY_DATABASE_URL

# worker
broker_url = f'amqp://{RabbitMQSettings.rabbitmq_username}:{RabbitMQSettings.rabbitmq_password}@{RabbitMQSettings.rabbitmq_host}:{RabbitMQSettings.rabbitmq_port}/{RabbitMQSettings.rabbitmq_port}'
# result_store
result_backend = SQLALCHEMY_DATABASE_URL
# result_backend = f'redis://{configs.REDIS_PASSWORD}@{configs.REDIS_HOST}:{configs.REDIS_PORT}/15'
# 用于存储计划的 Redis 服务器的 URL，默认为 broker_url的值
redbeat_redis_url = f'redis://:{RedisSettings.redis_password}@{RedisSettings.redis_host}:{RedisSettings.redis_port}/{RedisSettings.celery_beat_db}'
# 时区
timezone = 'Asia/Shanghai'
# UTC
enable_utc = False
# celery内容等消息的格式设置，默认json
accept_content = ['application/json', ]
task_serializer = 'json'
result_serializer = 'json'
# 为任务设置超时时间，单位秒。超时即中止，执行下个任务。
task_time_limit = 180
# 为存储结果设置过期日期，默认1天过期。如果beat开启，Celery每天会自动清除。设为0，存储结果永不过期
# result_expires = 300
# Worker并发数量，一般默认CPU核数，可以不设置
worker_concurrency = 5
# 每个worker执行了多少任务就会死掉，默认是无限的
# 防止内存泄漏
worker_max_tasks_per_child = 20
# 任务开始执行时更新任务的状态为 STARTED
task_track_started = True
# 断开重连
broker_connection_retry_on_startup = True
# 是否存储任务错误信息
task_store_errors_even_if_ignored = True
# 定时任务
beat_scheduler = 'redbeat.RedBeatScheduler'
# 任务前缀
# redbeat_key_prefix = 'redbeat:'
redbeat_key_prefix = f'{AppConfig.app_name}-redbeat:'
# RedBeat 使用分布式锁来防止多个实例同时运行。要禁用此功能，请设置：
# redbeat_lock_key = None
broker_transport_options = {
    'confirm_publish': True,
    'max_retries': 5,  # 最大重试次数
    'interval_start': 0,  # 提交任务时间，0代表立即开始
    'interval_step': 1,  # 每次重试多等的时间
}

beat_schedule = {}
