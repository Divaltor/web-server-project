FROM python:3.11-slim-bookworm

ENV PYTHONPATH "${PYTHONPATH}:/code"
ENV PATH "/code:${PATH}"

WORKDIR /code

RUN pip install poetry

COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi \
 && rm -rf $HOME/.cache

COPY . /code/