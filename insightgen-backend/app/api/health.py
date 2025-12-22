"""Health check endpoint"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns API status
    """
    return {
        "status": "healthy",
        "message": "InsightGen API is running"
    }
