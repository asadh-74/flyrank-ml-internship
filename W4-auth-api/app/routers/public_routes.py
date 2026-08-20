from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/info")
def info():
    return {"message": "Welcome stranger! This info is public."}
