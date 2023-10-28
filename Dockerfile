FROM python:3.9-alpine

# RUN apt-get update && apt-get install -y build-essential cmake

ENV PYTHON_VERSION=3.9 \
  APP_PATH=/home/python/app \
  POETRY_VIRTUALENVS_CREATE=false \
  PATH=/home/python/.local/lib/python3.9/site-packages:/usr/local/bin:/home/python:/home/python/app/bin:$PATH

# Install and configure dependencies
# RUN apk add --no-cache build-base libressl-dev musl-dev libffi-dev postgresql-dev
RUN pip install --no-cache-dir poetry

# Configure user, groups and working directory for application
RUN adduser -u 1000 -D python && \
  mkdir -p /home/python/app

WORKDIR /home/python/app

# RUN pip install --no-cache-dir -r base.txt
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

EXPOSE 5000

VOLUME [ "/home/python/app" ]


CMD ["python", "."]