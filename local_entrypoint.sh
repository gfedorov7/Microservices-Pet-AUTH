#!/bin/bash
set -e

echo "Waiting connect to PostgreSQL..."

until pg_isready -h auth_db -p 5432; do
  echo "Waiting access"
  sleep 1
done

echo "Database is available, run migrations"
poetry run alembic upgrade head

echo "Start uvicorn"
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
