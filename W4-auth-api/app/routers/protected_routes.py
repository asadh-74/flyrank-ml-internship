from fastapi import APIRouter, Depends

from ..deps import get_current_user

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("/profile")
def profile(current: dict = Depends(get_current_user)):
    user = current["user"]
    return {
        "id": user.id,
        "email": user.email,
        "created_at": str(user.created_at),
    }


@router.get("/dashboard")
def dashboard(current: dict = Depends(get_current_user)):
    """A second protected route proving the dependency is reusable, not
    copy-pasted — Stage 4's checkpoint."""
    user = current["user"]
    return {"message": f"Welcome back, {user.email}", "id": user.id}
