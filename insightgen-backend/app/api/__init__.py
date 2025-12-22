"""API package initialization"""
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router

__all__ = ["dashboard_router", "health_router"]
