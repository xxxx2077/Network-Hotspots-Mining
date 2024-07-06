from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# 设置环境变量，指定 Django 的配置文件模块位置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Network_Hotspots_Mining.settings')

# 创建 Celery 应用实例
app = Celery('Network_Hotspots_Mining')
# 从 Django 的设置文件导入 Celery 配置
app.config_from_object('django.conf:settings', namespace='CELERY')
# 定时任务
app.conf.beat_schedule = {
    'check_for_new_posts': {
        'task': 'app.tasks.LLM_summary_db',
        'schedule': crontab(minute='*/30'),  # 每30分钟执行一次
    },
}
# 自动发现并注册 Django 项目中所有的 Celery 任务
app.autodiscover_tasks()
