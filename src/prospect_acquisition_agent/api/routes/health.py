from fastapi import APIRouter

from src.prospect_acquisition_agent.models.health import HealthResponseModel

router = APIRouter()

@router.get("/health", tags=["health"])
async def health():
    return HealthResponseModel(status="UP")