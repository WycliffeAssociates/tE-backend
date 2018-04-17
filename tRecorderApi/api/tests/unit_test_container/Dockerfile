FROM python:3-slim-stretch

COPY . /tmp 

RUN apt-get update \
&& apt-get install ffmpeg \
&& cd /tmp \
&& pip install -r requirements.txt
