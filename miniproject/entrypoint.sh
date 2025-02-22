#!/bin/bash

# Wait for postgres
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - executing command"

case "$1" in
    "web")
        python manage.py migrate
        python manage.py runserver 0.0.0.0:8000
        ;;
    "celery")
        celery -A miniproject worker --loglevel=info
        ;;
    "celery-beat")
        celery -A miniproject beat --loglevel=info
        ;;
    *)
        exec "$@"
        ;;
esac 