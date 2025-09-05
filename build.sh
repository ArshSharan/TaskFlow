#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput --settings=taskmanager.settings_production
python manage.py migrate --settings=taskmanager.settings_production
