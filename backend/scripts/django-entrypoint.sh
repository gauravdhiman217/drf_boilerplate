#!/bin/bash

echo "Waiting for the database to be ready..."
python <<EOF
import time
import psycopg2
from psycopg2 import OperationalError

db_ready = False
while not db_ready:
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="$POSTGRES_USER",
            password="$POSTGRES_PASSWORD",
            host="$DB_HOST",
            port=int("$DB_PORT")
        )
        conn.close()
        db_ready = True
        print("Database is ready!")
    except OperationalError:
        print("Database is not ready. Retrying...")
        time.sleep(2)
EOF

echo "Database is ready!"


if [ $# -eq 0 ]; then
    echo "No arguments provided, skipping command execution."
    echo "Running Migration"
    python manage.py migrate

    echo "Populating Roles..."
    python manage.py loaddata fixtures/roles.json

    echo "Creating Admin User.."
    python manage.py populate_geo_data

    echo "Creating Superuser..."
    python manage.py createsuperuser --noinput 

    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    echo "Starting nginx..."
    nginx -g "daemon off;" &

    echo "Starting Gunicorn..."
    gunicorn core.wsgi --log-file - -b 127.0.0.1:8000 --reload --workers 2 --timeout 120 --max-requests 1000 --max-requests-jitter 50
else
    echo "Executing command: $@"
    exec "$@"
fi
 