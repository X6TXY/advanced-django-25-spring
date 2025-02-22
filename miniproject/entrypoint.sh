#!/bin/bash

# Wait for postgres
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - executing command"

case "$1" in
    "web")
        # Create migrations directory if it doesn't exist
        mkdir -p usersapp/migrations
        touch usersapp/migrations/__init__.py
        
        # Remove existing migrations and pyc files
        find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
        find . -path "*/migrations/*.pyc" -delete
        
        # Make fresh migrations for all apps
        python manage.py makemigrations
        
        # Apply migrations in the correct order
        python manage.py migrate --fake-initial
        python manage.py migrate auth
        python manage.py migrate admin
        python manage.py migrate contenttypes
        python manage.py migrate sessions
        python manage.py migrate usersapp
        python manage.py migrate tradingapp
        python manage.py migrate analyticsapp
        python manage.py migrate productsapp
        python manage.py migrate salesapp
        
        # Create superuser if it doesn't exist
        DJANGO_SUPERUSER_USERNAME=admin \
        DJANGO_SUPERUSER_EMAIL=admin@example.com \
        DJANGO_SUPERUSER_PASSWORD=admin \
        python manage.py createsuperuser --noinput || true
        
        # Start server
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