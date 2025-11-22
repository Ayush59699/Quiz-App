## flask api server:

> python3 app.py

## redis server (wsl)

> sudo service redis-server start

## MailHog Server

> cd backend
> ./MailHog

## Celery workers:

> celery -A app.celery worker -l info

## Celery Beat

> celery -A app.celery beat --max-interval 1 -l info

## AI Agent

> Set AIPROXY_TOKEN in .env file in root folder.

## Monthly report can only be downloaded if the user has attempted a quiz

## else gives 404 error

# if getting error of cffi, while starting flask server:

pip uninstall -y cryptography cffi
pip install --no-cache-dir cryptography cffi
