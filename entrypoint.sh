#!/bin/sh

set -e

echo "Running migrations..."
poetry run alembic upgrade head

echo "Adding users..."
poetry run python src/scripts/add_users.py

echo "Starting FastAPI app..."
exec poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload