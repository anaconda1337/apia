## APIA (Api Angelina)
- Example FastAPI following good practices and using the best tools for development.

## Features
- [x] FastAPI
- [x] Pydantic
- [x] Docker
- [x] Alembic
- [x] Postgres
- [x] Firebase
- [x] Pytest
- [ ] Flake8
- [ ] Mypy

## Requirements
- [ ] To be defined

## Installation
1. Bring up the database with docker-compose
```bash
docker compose up --build -d
```

2. Run the migrations
```bash
alembic upgrade head
```

3. Run the application
```bash
uvicorn app.main:app --reload
```

## Usage
- [ ] To be defined

## Notes
- Setup Firebase or remove the dependencies from the routes


## Curl

1. User IdToken from Firebase:
```bash
    curl --request POST \
      --url 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=[FIREBASE_API_KEY]' \
      --header 'Content-Type: application/json' \
      --data '{
      "email": "user@domain.tld",
      "password": "12345678",
      "returnSecureToken": true
    }'
```