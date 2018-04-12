#!/bin/bash
migrationspath=/tE-backend/tRecorderApi/api/migrations

if [ -d "$migrationspath" ]; then
	rm -rf "$migrationspath"
fi

mkdir "$migrationspath"
touch /tE-backend/tRecorderApi/api/migrations/__init__.py

cd /tE-backend/tRecorderApi/
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py jenkins --enable-coverage
