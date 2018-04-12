FROM python:3-slim-stretch

#WORKDIR /tE-backend/tRecorderApi

COPY . /tmp 

RUN apt-get update \
&& apt-get install ffmpeg \
	  postgresql \
		postgresql-client \
&& cd /tmp \
&& pip install -r requirements.txt

#ENTRYPOINT ["python3", "/tE-backend/tRecorderApi/manage.py", "jenkins", "--enable-coverage", "--settings=tRecorderApi.settings_test"]
