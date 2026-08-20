"""
Supabase client + the reusable auth guard.

This is the one module every protected route depends on. Stage 4 of the
assignment asks for the token-checking logic to live in ONE place instead of
being copy-pasted into every route — this is that place.
"""
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

# Anon-key client: used for signup/login and for verifying tokens (get_user).
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Optional service-role client: only needed so /auth/logout can actually
# revoke the session server-side (supabase.auth.sign_out() on the anon
# client can't invalidate someone else's token — only the admin API can).
# If SUPABASE_SERVICE_KEY isn't set, logout still returns 204 but is a
# client-side "forget the token" logout rather than a server-side revoke.
admin_client: Client | None = None
if SUPABASE_SERVICE_KEY:
    admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# HTTPBearer is what makes FastAPI draw the "Authorize" padlock in Swagger
# UI (/docs) and attach the bearer security scheme to any route that
# depends on it. auto_error=False lets us return our own 401 JSON shape
# instead of FastAPI's default.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    """
    Dependency for every protected route.

    - No header / malformed header -> 401 "Access token required"
    - Header present but Supabase rejects it (expired/tampered/invalid)
      -> 401 "Invalid or expired token"
    - Valid -> returns {"user": <supabase user>, "token": <raw jwt>}
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Access token required")

    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if response is None or response.user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"user": response.user, "token": token}
