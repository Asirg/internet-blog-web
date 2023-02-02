#!/bin/sh

python manage.py flush --no-input
python manage.py migrate

python manage.py createsuperuser --no-input

python manage.py collectstatic --no-input --clear

exec "$@"

