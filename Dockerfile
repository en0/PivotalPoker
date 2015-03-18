FROM ubuntu:14.04


RUN apt-get --fix-missing update
RUN apt-get install -y supervisor redis-server python python-flask python-redis

VOLUME /srv/http

ADD src/ /srv/http
ADD conf.d/ /etc/supervisor/conf.d/

CMD supervisord -n
