#!/bin/sh

# Wait for the database to be ready
echo "Waiting for the database to be ready."
scripts/wait-script.sh db:5432 --timeout=60 -- echo "Database is ready."

echo "Running Migration"
python manage.py migrate

echo "Populating Roles..."
python manage.py loaddata fixtures/roles.json

echo "Populating User Data..."
python manage.py seed

# echo "Creating Superuser..."
# python manage.py createsuperuser --noinput 

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"