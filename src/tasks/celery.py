from celery import Celery
import asyncio

import settings
from services.services import process_posts_with_prize_draws_from_database, add_posts_from_tracking_accounts_to_db


redis_path = f'redis://{settings.CONFIG['redis']['url']}/0'

app = Celery('reposting', backend=redis_path, broker=redis_path)
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()
app.conf.update(
    task_serializer="json", result_serializer="json", accept_content=["json"]
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    frequency_of_reposts_in_seconds = 10800.0
    sender.add_periodic_task(frequency_of_reposts_in_seconds, \
                              repost.s(), name='Periodic repost')


@app.task
def repost():
    asyncio.run(add_posts_from_tracking_accounts_to_db())
    return asyncio.run(process_posts_with_prize_draws_from_database())
