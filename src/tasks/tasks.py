from celery import Celery, shared_task
from services.services import get_posts_from_tracking_account, repost_all_new_posts_from_database

app = Celery('tasks', backend='redis://localhost:6379',
                broker='redis://localhost:6379')

@shared_task()
async def search_and_repost_posts(message):
    await get_posts_from_tracking_account(message)
    await repost_all_new_posts_from_database(message)