FROM python:3.10-slim

ARG app_version=0.0.0
ENV APP_VERSION=${app_version}

ENV APP /service
ENV PYTHONPATH /service
WORKDIR $APP

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

COPY requirements/base.txt $APP
RUN pip install -r base.txt --no-cache


COPY . $APP
ENTRYPOINT ["./entrypoint.sh"]
