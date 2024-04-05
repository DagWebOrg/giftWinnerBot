# Makefile
celery-worker:
	celery -A tasks.celery.app worker --loglevel=info --pool=solo
celery-beat:
	celery -A tasks.celery.app beat --loglevel=info

