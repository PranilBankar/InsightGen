"""Dashboard API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import DashboardRequest, DashboardResponse, ErrorResponse
from app.services import dashboard_builder
from app.security import limiter
from fastapi import Request

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.post(
    "/generate",
    response_model=DashboardResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
@limiter.limit("10/minute")
async def generate_dashboard(
    request: Request,
    dashboard_request: DashboardRequest,
    db: Session = Depends(get_db)
):
    """
    Generate dashboard from natural language query
    
    **Example Request:**
    ```json
    {
        "query": "Show sales trends by category for last quarter"
    }
    ```
    
    **Returns:**
    - Complete dashboard with charts, insights, and metadata
    """
    try:
        # Build dashboard
        dashboard = dashboard_builder.build_dashboard(
            db=db,
            user_question=dashboard_request.query
        )
        
        return dashboard
        
    except ValueError as e:
        # Validation errors (SQL validation, etc.)
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        # Internal errors
        raise HTTPException(
            status_code=500,
            detail=f"Dashboard generation failed: {str(e)}"
        )
