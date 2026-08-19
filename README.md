# Task CRUD API — FlyRank Backend Week 2

## Assignment
**Week 2 — Assignment A1: Build your first CRUD API**

A small To-Do API built with **Python + FastAPI**. It implements Create, Read, Update and Delete using an in-memory list.

## Features
- GET `/` — API information
- GET `/health` — health check
- GET `/tasks` — list tasks
- GET `/tasks/{id}` — get one task
- POST `/tasks` — create task
- PUT `/tasks/{id}` — update task
- DELETE `/tasks/{id}` — delete task
- GET `/stats` — optional extra
- Input validation and JSON errors
- Swagger UI automatically available at `/docs`

## Run
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:
- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## Endpoint table

| Method | Endpoint | Purpose | Success |
|---|---|---|---|
| GET | `/` | API information | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | List tasks | 200 |
| GET | `/tasks/{id}` | Get one task | 200 |
| POST | `/tasks` | Create task | 201 |
| PUT | `/tasks/{id}` | Update task | 200 |
| DELETE | `/tasks/{id}` | Delete task | 204 |
| GET | `/stats` | Statistics extra | 200 |

## Test commands

```bash
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/tasks
curl -i http://127.0.0.1:8000/tasks/1
curl -i http://127.0.0.1:8000/tasks/99
```

Create:
```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

Update:
```bash
curl -i -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d "{\"title\":\"Learn FastAPI\",\"done\":true}"
```

Delete:
```bash
curl -i -X DELETE http://127.0.0.1:8000/tasks/1
```

## Validation
- Missing/empty title on POST → 400
- Empty update body → 400
- Empty title on PUT → 400
- Unknown ID → 404
- Successful delete → 204

## In-memory note
Tasks are stored in a Python list. Restarting the server resets the data. No database is used.

## Submission checklist
- [x] Full CRUD API
- [x] In-memory storage
- [x] Correct status codes
- [x] POST/PUT validation
- [x] Swagger UI
- [x] README
- [x] Optional stats endpoint
- [ ] Push to a public GitHub repository
- [ ] Make at least 6 meaningful commits
- [ ] Add a Swagger screenshot to README

## Suggested Git commits
1. `Stage 0: hello server`
2. `Stage 1: root and health endpoints`
3. `Stage 2: read endpoints with 404`
4. `Stage 3: create with validation`
5. `Stage 4: full CRUD`
6. `Stage 5: Swagger UI`
7. `Stage 6: publish and docs`

## Bonus — AI Rematch
Prompt used:
> Build a Python FastAPI To-Do CRUD API using an in-memory list. Include GET `/`, GET `/health`, GET `/tasks`, GET `/tasks/{id}`, POST `/tasks`, PUT `/tasks/{id}`, and DELETE `/tasks/{id}`. Use numeric id, title and done fields. POST creates the next ID and returns 201. Unknown IDs return 404. PUT updates title and/or done, rejects invalid input with 400, and DELETE returns 204. Include FastAPI Swagger UI at `/docs`. Do not use a database or files.

Review points:
1. Validation is explicit for empty titles and empty PUT bodies.
2. Status codes are handled as required: 201, 204, 400 and 404.
3. Storage remains in memory.
4. Swagger/OpenAPI is provided by FastAPI.
