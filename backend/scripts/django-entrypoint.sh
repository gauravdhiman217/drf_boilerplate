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


echo "Running Migration"
python manage.py migrate

echo "Populating Roles..."
python manage.py loaddata fixtures/roles.json

# echo "Populating User Data..."
# python manage.py seed

echo "Creating Superuser..."
python manage.py createsuperuser --noinput 

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"