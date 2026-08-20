from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .routers import auth_routes, protected_routes, public_routes

app = FastAPI(
    title="Auth API",
    description="Sign up, log in, and protect routes using Supabase Auth.",
    version="1.0.0",
)


@app.on_event("startup")
async def on_startup():
    print("Server running and connected to Supabase")


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request, exc: RequestValidationError):
    # Missing/empty email or password -> 400 with a plain { "error": ... }
    # body, instead of FastAPI's default 422 shape.
    return JSONResponse(
        status_code=400, content={"error": "email and password are required"}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    # Every error in this API — 400, 401, 404 — comes back as { "error": ... }
    # instead of FastAPI's default { "detail": ... }.
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


app.include_router(auth_routes.router)
app.include_router(public_routes.router)
app.include_router(protected_routes.router)
