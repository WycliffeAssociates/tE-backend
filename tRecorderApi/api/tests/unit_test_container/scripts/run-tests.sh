#!/usr/bin/env bash

#This script is for running the tests for the environment defined in test-runner.yml
#The environment variables used in this script are defined in test-runner.env

rm -rf /tE-backend/tRecorderApi/api/migrations 
mkdir /tE-backend/tRecorderApi/api/migrations
touch /tE-backend/tRecorderApi/api/migrations/__init__.py
cd /tE-backend/tRecorderApi
python3 manage.py makemigrations
python3 manage.py migrate
coverage run \
	--source="api"\
	--omit='**test**' \
	manage.py test api
coverage xml
