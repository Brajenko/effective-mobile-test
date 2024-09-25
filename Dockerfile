FROM python:3.12-slim

RUN pip install poetry

COPY . .

RUN poetry install

WORKDIR /backend

ENTRYPOINT ["poetry", "run", "python", "-m", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0", "main:app"]
