from celery.schedules import crontab
from celery import Celery, shared_task
from services.services import get_posts_from_tracking_account, repost_all_new_posts_from_database

app = Celery('tasks', backend='redis://localhost:6379',
                broker='redis://localhost:6379')

@app.task
def search_and_repost_posts():
    await get_posts_from_tracking_account()
    await repost_all_new_posts_from_database()


app.conf.beat_schedule = {
    'repost': {
        'task': 'tasks.search_and_repost_posts',
        'schedule': 7200.0,
    },
}
