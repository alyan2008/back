FROM ubuntu:14.04
MAINTAINER Andrii Dvoiak
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update
RUN apt-get install -y python-pip python-dev python-lxml libxml2-dev libxslt1-dev libxslt-dev libpq-dev zlib1g-dev && apt-get build-dep -y python-lxml && apt-get clean
# Specify your own RUN commands here (e.g. RUN apt-get install -y nano)

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /project

EXPOSE 80
