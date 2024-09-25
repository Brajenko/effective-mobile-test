# My Effective Mobile test task completion

## Run with docker
```bash
docker compose up
```

## Run without docker
```bash
poetry install --no-dev
cd backend
./run
```

## Local development setup
```bash
poetry install
alembic upgrade head
```

## Running tests
```bash
cd backend
pytest
```
