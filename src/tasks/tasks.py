from celery.schedules import crontab
from celery import Celery, shared_task
from services.services import get_posts_from_tracking_account, repost_all_new_posts_from_database

app = Celery('tasks', backend='redis://localhost:6379',
                broker='redis://localhost:6379')

@app.task
def search_and_repost_posts():
    print('aaa')
    # await get_posts_from_tracking_account()
    # await repost_all_new_posts_from_database()


beat_schedule = {
    'repost_morning': {
        'task': 'search_and_repost_posts',
        'schedule': crontab(hour=16, minute=51),
    },
    'repost_evening': {
        'task': 'search_and_repost_posts',
        'schedule': crontab(hour=16, minute=50),
    },
}