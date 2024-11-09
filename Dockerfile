FROM python:3.12

WORKDIR /test

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .
CMD poetry shell

