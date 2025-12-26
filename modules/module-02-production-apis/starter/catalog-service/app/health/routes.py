from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def live() -> dict:
    return {"status": "ok"}


@router.get("/ready")
def ready() -> dict:
    # In later modules, this becomes real checks (DB connectivity, dependency health, etc.)
    return {"status": "ok"}


