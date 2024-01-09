FROM python:3.11

WORKDIR /var/www/app

COPY ./pyproject.toml /var/www/app/pyproject.toml
COPY ./poetry.lock /var/www/app/poetry.lock

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install --no-root

COPY ./src /var/www/app/src

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
