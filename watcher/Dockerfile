FROM python:3.12

WORKDIR /watcher

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .

CMD poetry run python -u -m watcher.main
