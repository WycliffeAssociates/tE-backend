cd /tE-backend/tRecorderApi
python3 manage.py makemigrations --settings-tRecorderApi.settings_test
python3 manage.py migrate --settings=tRecorderApi.settings_test
python3 manage.py jenkins --enable-coverage --settings=tRecorderApi.settings_test
