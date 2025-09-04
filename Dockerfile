FROM python:3.13

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root --only main

COPY . .

CMD ["python", "manage.py", "runserver"]
