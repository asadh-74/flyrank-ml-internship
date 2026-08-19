# Task API — containerized with Postgres (A3)

A small task CRUD API, backed by a real PostgreSQL database running in
Docker. App and database start together with one command.

This is the third storage swap on the same API: in-memory → SQLite →
Postgres (this one). The routes never changed — only `app/repository.py`
did, which is the whole point: storage is an implementation detail.

## Run it

```bash
cp .env.example .env
docker compose up
```

That's it. The API is now at `http://localhost:3000`, backed by Postgres
running in its own container, with three example tasks already seeded.

To confirm it's alive:

```bash
curl -i http://localhost:3000/health
```

## Environment variables

Set in `.env` (gitignored — never commit real credentials). See
`.env.example` for the keys you need:

| Variable       | Meaning                                  |
|----------------|-------------------------------------------|
| `DATABASE_URL` | Postgres connection string for the app    |

Note: `.env` is only used when running the app **outside** compose (e.g.
locally against `docker run ... postgres`). Inside `docker-compose.yml`,
`DATABASE_URL` is injected directly by the `api` service definition and
points at the `db` service by name, not `localhost`.

## Endpoints

| Method | Path           | Body                          | Success       | Errors                        |
|--------|----------------|--------------------------------|---------------|--------------------------------|
| GET    | `/tasks`       | —                              | `200`         | —                              |
| GET    | `/tasks/{id}`  | —                              | `200`         | `404` unknown id               |
| POST   | `/tasks`       | `{"title": str, "done": bool}` | `201`         | `400` missing/empty title      |
| PUT    | `/tasks/{id}`  | `{"title": str, "done": bool}` | `200`         | `400` invalid body, `404` id   |
| DELETE | `/tasks/{id}`  | —                              | `204`         | `404` unknown id               |
| GET    | `/health`      | —                              | `200`         | `503` if the DB is unreachable |

All errors are returned as `{"error": "message"}`.

### Example

```bash
curl -i http://localhost:3000/tasks
```

```
HTTP/1.1 200 OK
content-type: application/json

[{"id":1,"title":"Buy groceries","done":false},
 {"id":2,"title":"Write report","done":false},
 {"id":3,"title":"Walk the dog","done":true}]
```

## Architecture: why the routes never change

`app/repository.py` is the **only** module that talks to Postgres — every
query is parameterized (`%s` placeholders; user input is always passed
separately, never string-glued into SQL). `app/main.py` calls repository
methods and knows nothing about SQL, connection pools, or Postgres. That
separation is what let three different storage engines (memory → SQLite →
Postgres) sit under an identical API across this project's assignments —
swapping storage only ever touched this one file.

## Persistence, proven

Data survives a full stack restart because Postgres writes to a named
Docker volume (`taskdata`), not the container's writable layer:

```bash
# create a task
curl -s -X POST localhost:3000/tasks -H 'content-type: application/json' \
  -d '{"title":"survive a restart"}'

# take the whole stack down and back up
docker compose down
docker compose up -d

# it's still there
curl -s localhost:3000/tasks
```

If you instead `docker compose down -v` (which also deletes volumes), the
data is gone — that's the volume doing its job, not a bug.

## Project layout

```
app/
  main.py         # FastAPI app, routes, error formatting
  repository.py   # the only module that speaks SQL
  db.py           # connection pool, reads DATABASE_URL
  schemas.py      # request/response models
sql/init.sql      # reference copy of the schema (app creates it automatically)
Dockerfile        # builds the api image
docker-compose.yml
.env.example
```

## Stretch ideas (not implemented here)

- **Redis**: add a `redis` service to `docker-compose.yml` and ping it
  once at startup — useful ahead of a later caching assignment.
- **Index + EXPLAIN ANALYZE**: add `CREATE INDEX ON tasks (done);`, seed a
  larger table, and compare `EXPLAIN ANALYZE SELECT * FROM tasks WHERE
  done = true;` before/after to see the plan change from a sequential
  scan to an index scan.
