#!/bin/bash
# Render build script for Bloodlink backend deployment
# This script runs automatically on Render deployment

set -o errexit

echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running database migrations..."
python manage.py migrate

echo "Build complete!"

