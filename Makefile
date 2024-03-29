# Makefile
celery-start-worker:
	celery -A tasks.tasks.app worker --loglevel=info

celery-beat:
	celery -A tasks.tasks.app beat -l info --schedule='tasks.scheduler.beat_schedule'
