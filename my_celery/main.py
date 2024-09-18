from __future__ import absolute_import
import os
import traceback
from config.env import AppConfig
from celery import Celery
from celery.signals import task_postrun
from dotenv import load_dotenv
from settings.db import SessionLocal

load_dotenv()


def make_celery():
    # 实例化
    app = Celery(
        AppConfig.app_name, include=[]
    )
    # 加载celery配置文件
    app.config_from_object('my_celery.config')

    return app


celery_app = make_celery()

if __name__ == '__main__':
    args = ['worker', '--loglevel=INFO']
    celery_app.worker_main(argv=args)
