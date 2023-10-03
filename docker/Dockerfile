FROM python:3.10

RUN groupadd -r backend && useradd --no-log-init -r -g backend backend

WORKDIR /backend

# set python environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set system environment variables
ENV POETRY_VERSION=1.1.13
ENV DJANGO_SETTINGS_MODULE=example_docker.settings
ENV POETRY_VERSION=1.3.*
ENV DJANGO_SETTINGS_MODULE=backend.settings

# install dependencies
RUN pip install --ignore-installed "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock /backend/
RUN POETRY_VIRTUALENVS_CREATE=false poetry install

USER backend

# expose port so that you can access webserver on local machine
EXPOSE 8000
