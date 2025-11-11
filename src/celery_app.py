from datetime import timedelta

from celery import Celery

from src.settings import settings

redis = settings.redis

app = Celery(
    'notification_service',
    broker=redis.REDIS_URL,
    backend=redis.REDIS_URL,
    include=['src.tasks.notifications'],
)

app.conf.update(
    timezone='Europe/Moscow',
    enable_utc=True,
    task_default_queue='default',
    beat_schedule={
        'send-notifications-every-second': {
            'task': 'src.tasks.notifications.send_notifications',
            'schedule': timedelta(seconds=5),
        },
    },
)
