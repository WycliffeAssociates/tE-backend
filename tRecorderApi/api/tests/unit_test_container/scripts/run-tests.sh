rm -rf /tE-backend/tRecorderApi/api/migrations 
mkdir /tE-backend/tRecorderApi/api/migrations
touch /tE-backend/tRecorderApi/api/migrations/__init__.py
cd /tE-backend/tRecorderApi
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py jenkins \
	--enable-coverage \
	--coverage-exclude='api.tests' \
	--coverage-format=xml,html
