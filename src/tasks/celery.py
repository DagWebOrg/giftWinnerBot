from celery import Celery
from services.services import repost_all_new_posts_from_database, add_all_new_posts_to_database
import asyncio

app = Celery('reposting', backend='redis://localhost:6379/0',
                broker='redis://localhost:6379/0')

app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()
app.conf.update(
    task_serializer="json", result_serializer="json", accept_content=["json"]
)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(60.0, repost.s(), name='Run every second')
    # sender.add_periodic_task(crontab(minute=0, hour=12), repost.s(), name='Morning repost')
    # sender.add_periodic_task(crontab(minute=17, hour=17), repost.s(), name='Evening repost')


@app.task
def repost():
    asyncio.run(add_all_new_posts_to_database())
    return asyncio.run(repost_all_new_posts_from_database())
