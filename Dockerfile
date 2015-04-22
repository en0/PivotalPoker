FROM ubuntu:14.04

RUN apt-get --fix-missing update
RUN apt-get install -y supervisor redis-server python python-flask python-redis gunicorn
RUN mkdir -p /srv/http

ADD src/ /srv/http
ADD conf.d/ /etc/supervisor/conf.d/
add poker.conf /etc/poker.conf

ENV PIVOTALPOKER_CONFIG /etc/poker.conf
CMD supervisord -n
