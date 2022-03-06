#!/bin/bash
set -e
cd db_model/alembic && alembic upgrade head
exec uvicorn main:app --host 0.0.0.0 --port 80
exec "$@"
