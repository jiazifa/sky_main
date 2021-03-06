FROM python:3.7

ARG pypi_host=pypi.douban.com
ARG pypi_mirror=http://pypi.douban.com/simple

ENV LC_ALL C.UTF-8

ENV LANG C.UTF-8

ENV PIP_INDEX_URL $pypi_mirror

ENV FLASK_ENV product

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt --trusted-host ${pypi_host}

COPY app app

COPY migrations migrations

COPY celery_worker.py celery_worker.py

COPY start_server.sh start_server.sh

COPY runner.py runner.py

RUN chmod a+x start_server.sh

EXPOSE 5000
