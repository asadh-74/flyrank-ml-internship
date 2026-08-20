# Auth API — Login & Protect

A FastAPI service that hands off authentication to Supabase: sign up, log in,
get a JWT, and use it to access protected routes. Built for FlyRank
Internship assignment **BE-03**.

## What this is

- `POST /auth/signup`, `POST /auth/login`, `POST /auth/logout` — Supabase
  handles the actual accounts and password hashing; this API is a thin,
  correctly-shaped layer on top of it.
- `GET /protected/profile`, `GET /protected/dashboard` — return 401 unless a
  valid Supabase-issued JWT is sent as `Authorization: Bearer <token>`.
- `GET /public/info` — no auth required.
- All token-checking logic lives in **one dependency**
  (`app/deps.py::get_current_user`), applied to every protected route instead
  of duplicated per-route.

## Setup

1. Create a free project at [supabase.com](https://supabase.com).
2. In **Project Settings → API**, copy the **Project URL** and **anon public
   key**.
3. Copy the example env file and fill in your values:
   ```bash
   cp .env.example .env
   ```
   ```
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   SUPABASE_SERVICE_KEY=your_service_role_key   # optional, see note below
   PORT=8000
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run it:
   ```bash
   python run.py
   ```
   You should see `Server running and connected to Supabase` in the console.
   API docs are at **http://localhost:8000/docs**.

> **Note on `SUPABASE_SERVICE_KEY`:** it's optional. Without it, `/auth/logout`
> still returns `204`, but it can only sign out the local anon client — it
> can't force-revoke that specific user's session server-side, because JWTs
> are stateless and revoking someone else's session requires the admin API
> (service-role key). With the service key set, logout calls
> `admin_client.auth.admin.sign_out(token)` for a real server-side revoke.

## API reference

| Method | Route                  | Auth required | Purpose                          |
|--------|-------------------------|:---:|-----------------------------------|
| POST   | `/auth/signup`          | No  | Create a new user account         |
| POST   | `/auth/login`           | No  | Log in, get back access/refresh tokens |
| POST   | `/auth/logout`          | Yes | End the session                   |
| GET    | `/public/info`          | No  | Public, unprotected data          |
| GET    | `/protected/profile`    | Yes | Read the caller's own profile     |
| GET    | `/protected/dashboard`  | Yes | Second protected route, proves the auth dependency is reusable |

**Status codes:** `201` signup, `200` login/read, `204` logout, `400`
missing/invalid input, `401` missing/invalid/expired token.

## Example

```bash
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
# → { "access_token": "...", "refresh_token": "...", "token_type": "bearer" }

curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <access_token>"
```

## Swagger UI

`/docs` shows a padlock icon on every protected route (FastAPI picks this up
automatically from the `HTTPBearer` dependency in `app/deps.py`). Click
**Authorize**, paste your access token, and try `/protected/profile` directly
from the browser.

*(Screenshot of `/docs` with the Authorize dialog goes here.)*

## Project structure

```
app/
  deps.py               # Supabase clients + the one auth dependency
  schemas.py             # request bodies (Pydantic)
  main.py                 # app instance, routers, error shaping
  routers/
    auth_routes.py        # signup / login / logout
    public_routes.py       # /public/info
    protected_routes.py     # /protected/profile, /protected/dashboard
run.py                     # entrypoint, reads PORT from .env
```

## AI vs Me

*(Fill in after running Stage 7 — the bonus AI rematch. Prompt an AI
assistant to build the same spec in a separate `ai-version/` folder, run it,
and note here how it handled Bearer-prefix parsing, whether it introduced any
security flaws, and what your prompt left unspecified.)*
