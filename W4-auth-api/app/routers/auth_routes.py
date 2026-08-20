from fastapi import APIRouter, Depends, HTTPException

from ..deps import admin_client, get_current_user, supabase
from ..schemas import LoginIn, SignupIn

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=201)
def signup(body: SignupIn):
    try:
        result = supabase.auth.sign_up(
            {"email": body.email, "password": body.password}
        )
    except Exception as exc:
        # Supabase raises for things like "user already registered",
        # weak password, etc. Surface it as a 400, not a 500.
        raise HTTPException(status_code=400, detail=str(exc))

    if result.user is None:
        raise HTTPException(status_code=400, detail="Signup failed")

    return {
        "id": result.user.id,
        "email": result.user.email,
        "created_at": str(result.user.created_at),
    }


@router.post("/login")
def login(body: LoginIn):
    try:
        result = supabase.auth.sign_in_with_password(
            {"email": body.email, "password": body.password}
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    if result.session is None:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return {
        "access_token": result.session.access_token,
        "refresh_token": result.session.refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout", status_code=204)
def logout(current: dict = Depends(get_current_user)):
    token = current["token"]
    try:
        if admin_client is not None:
            # True server-side revoke — requires SUPABASE_SERVICE_KEY.
            admin_client.auth.admin.sign_out(token)
        else:
            # Falls back to a local sign-out on the anon client. The token
            # itself stays valid until it expires; this is a known
            # limitation of stateless JWTs without a service-role key.
            supabase.auth.sign_out()
    except Exception:
        # Logout should be idempotent from the client's point of view —
        # don't fail the request just because the session was already gone.
        pass
    return
