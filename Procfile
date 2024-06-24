web: gunicorn onlinestore.wsgi:application
worker: celery -A onlinestore.celery worker --pool=solo -l info
beat: celery -A onlinestore beat -l info