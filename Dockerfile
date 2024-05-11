FROM python:3.10-alpine

LABEL maintainer="kamil.alimetov@gmail.com"

COPY . /giftWinnerBot
WORKDIR /giftWinnerBot/src

RUN apk update
RUN pip install -r ../requirements.txt
RUN apk add --no-cache supervisor
RUN apk add make

COPY supervisord.conf /etc/supervisord.conf


CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]



