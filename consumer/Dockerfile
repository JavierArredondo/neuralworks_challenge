FROM python:3.8-slim

RUN apt-get -y update

WORKDIR /app
COPY . /app

RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
