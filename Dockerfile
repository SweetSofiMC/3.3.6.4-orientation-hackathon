FROM python:3.8-slim-buster

RUN mkdir /myportfolio
COPY requirements.txt /myportfolio
WORKDIR /myportfolio
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install -r requirements.txt

COPY . /myportfolio

RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]
