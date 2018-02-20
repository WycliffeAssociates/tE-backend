FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

# FFMPEG
#The repository needs updating from the original
#Note that ffmpeg not standardly available for Ubuntu 14.04: http://www.faqforge.com/linux/how-to-install-ffmpeg-on-ubuntu-14-04/
RUN echo "deb http://httpredir.debian.org/debian jessie-backports main non-free\n" >> /etc/apt/sources.list
RUN echo "deb-src http://httpredir.debian.org/debian jessie-backports main non-free\n" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y ffmpeg



RUN pip install -r requirements.txt
ADD . /code/
