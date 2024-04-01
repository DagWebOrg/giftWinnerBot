from celery.schedules import crontab
from tasks import app


beat_schedule = {
    'repost_morning': {
        'task': 'tasks.search_and_repost_posts',
        'schedule': crontab(hour=16, minute=51),
    },
    'repost_evening': {
        'task': 'tasks.search_and_repost_posts',
        'schedule': crontab(hour=16, minute=50),
    },
}