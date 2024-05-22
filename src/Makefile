# Makefile
celery-worker:
	celery -A tasks.celery.app worker --loglevel=info --pool=solo --logfile=logger/logs/worker.log -E
celery-beat:
	celery -A tasks.celery.app beat --loglevel=info --logfile=logger/logs/beat.log

