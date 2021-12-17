FROM python:3.8.1-buster

ADD . /opt/tg_bot

WORKDIR /opt/tg_bot

VOLUME . /opt/tg_bot

CMD [ "python", "-m", "bot"]
