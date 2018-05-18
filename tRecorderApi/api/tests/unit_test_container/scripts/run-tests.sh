#!/usr/bin/env bash

#This script is for running the tests for the environment defined in test-runner.yml
#The environment variables used in this script are defined in test-runner.env

rm -rf $MIGRATIONS_DIR 
mkdir $MIGRATIONS_DIR 
mkdir $COVERAGE_DIR
touch $MIGRATIONS_INIT 
cd /tE-backend/tRecorderApi
python3 manage.py makemigrations
python3 manage.py migrate
coverage run \
	--source="api"\
	--omit='**test**' \
	manage.py test api
coverage xml
