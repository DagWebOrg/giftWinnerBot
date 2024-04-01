# Makefile
celery-start-worker:
	celery -A tasks.tasks.app worker -B --schedule='tasks.tasks.beat_schedule' --loglevel=info --logfile=celery_worker.log -E
celery-beat:
	celery -A tasks.tasks.app beat -l info --schedule='tasks.scheduler.beat_schedule' --logfile=celery_beat.log
