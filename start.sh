#!/bin/sh
docker pull postgres:latest
docker start postgres
if [ $? -ne 0 ]; then
    docker run --name postgres -v volumes:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 postgres
fi

export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
uvicorn app.main:app --reload --port 8000