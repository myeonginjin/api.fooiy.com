#!/bin/bash

if [ "celery" = "$1" ]
then
    celery -A fooiy worker --loglevel=info
else
    echo "*--------MAKE LOGS FOLDER---------*"
    touch /srv/logs/gunicorn.log
    touch /srv/logs/access.log
    chmod 777 -R /srv/logs
    tail -n 0 -f /srv/logs/*.log &

    echo "*--------DJANGO MIGRATION---------*"
    # python3 manage.py makemigrations --noinput --merge
    # python3 manage.py makemigrations --noinput
    # python3 manage.py makemigrations 
    # python3 manage.py migrate
    # python3 manage.py migrate --fake
    # python3 manage.py collectstatic --noinput

    echo "*--------TEST---------*"
    # python3 manage.py test
    # coverage erase
    # coverage run manage.py test
    # coverage report

    echo "*--------START GUNICORN PROCESS---------*"
    exec gunicorn fooiy.wsgi:application \
        --name fooiy \
        --bind unix:django_app.sock \
        --workers 3 \
        --timeout 300 \
        --log-level=info \
        --log-file=/srv/logs/gunicorn.log \
        --access-logfile=/srv/logs/access.log &

    echo "*--------START NGINX---------*"
    exec service nginx start
fi