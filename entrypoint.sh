#!/bin/sh
# entrypoint.sh
echo "Applying migrations..."
python3 manage.py migrate
echo "Migrations applied."

exec "$@"