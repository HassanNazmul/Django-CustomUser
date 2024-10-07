#!/bin/bash

# Ensure script fails if any command fails
set -e

echo "Making Migrations ..."
python manage.py makemigrations

echo "Applying Migrations ..."
python manage.py migrate

echo "Migrations completed successfully!"


