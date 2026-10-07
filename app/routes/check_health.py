from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def check_health() -> dict[str, str]:
    return {"status": "ok"}
