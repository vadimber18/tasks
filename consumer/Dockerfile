FROM python:3.10-slim

ARG app_version=0.0.0
ENV APP_VERSION=${app_version}

ENV APPLICATION /consumer
ENV PYTHONPATH /consumer
WORKDIR $APPLICATION

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

COPY requirements/base.txt $APP_
RUN pip install -r base.txt --no-cache


COPY . $APPLICATION

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]