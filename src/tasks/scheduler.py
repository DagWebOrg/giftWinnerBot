from celery.schedules import crontab


beat_schedule = {
    'repost_morning': {
        'task': 'tasks.tasks.search_and_repost_posts',
        'schedule': crontab(hour=16, minute=17),
    },
    'repost_evening': {
        'task': 'tasks.tasks.search_and_repost_posts',
        'schedule': crontab(hour=20, minute=30),
    },
}