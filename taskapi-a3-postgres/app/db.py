"""
Database connection setup.

Reads DATABASE_URL from the environment (populated from .env locally,
or injected directly by docker-compose in the container). Never hardcode
credentials here.
"""
import os

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

# Only useful when running outside docker-compose (compose injects env vars
# directly). Harmless no-op if .env doesn't exist.
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Copy .env.example to .env and fill it in."
    )

# autocommit=True keeps the repository layer simple (no manual conn.commit()
# after every write) which is fine for this small CRUD service.
pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=5,
    kwargs={"autocommit": True},
    open=True,
)
