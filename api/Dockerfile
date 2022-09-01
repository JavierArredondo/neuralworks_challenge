FROM python:3.8

RUN apt-get -y update

ADD requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install gunicorn && pip install psycopg2-binary
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 5000

ENV APP_WORKERS="1"
ENV APP_THREADS="1"

CMD ["/bin/bash", "scripts/entrypoint.sh"]
