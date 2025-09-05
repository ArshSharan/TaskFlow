#!/usr/bin/env bash
# Build script for Render deployment

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input --settings=taskmanager.settings_render

# Run migrations
python manage.py migrate --settings=taskmanager.settings_render
