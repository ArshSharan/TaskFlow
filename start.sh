#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE=taskmanager.settings_production
exec gunicorn taskmanager.wsgi:application --bind 0.0.0.0:$PORT
