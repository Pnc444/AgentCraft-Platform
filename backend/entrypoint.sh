#!/bin/sh
set -e

echo "Waiting for database..."
until python -c "
import os, sys, psycopg2
try:
    psycopg2.connect(os.environ['DATABASE_URL'])
    sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(1)
" 2>/dev/null; do
  echo "Database not ready, retrying..."
  sleep 2
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec "$@"
