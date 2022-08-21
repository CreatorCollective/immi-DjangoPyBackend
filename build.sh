#!/usr/bin/env bash
# exit on error
set -o errexit

curl -sSL https://install.python-poetry.org | python3 - --version 1.2.0b2
poetry install

python manage.py collectstatic --no-input
python manage.py migrate
