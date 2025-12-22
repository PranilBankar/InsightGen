"""Pydantic schemas for API request/response validation"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class DashboardRequest(BaseModel):
    """Request model for dashboard generation"""
    query: str = Field(
        ..., 
        description="Natural language question",
        min_length=3,
        max_length=500,
        examples=["Show sales trends by category for last quarter"]
    )


class ChartConfig(BaseModel):
    """Chart configuration"""
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    group_by: Optional[str] = None
    aggregation: str = "none"


class Chart(BaseModel):
    """Chart model"""
    id: str
    type: str = Field(..., description="Chart type: line, bar, pie, area, scatter")
    title: str
    data: List[Dict[str, Any]]
    config: ChartConfig


class DashboardMetadata(BaseModel):
    """Dashboard metadata"""
    rows_returned: int
    execution_time_ms: float
    columns: List[str]


class DashboardResponse(BaseModel):
    """Response model for dashboard generation"""
    dashboard_id: str
    query: str
    sql: str
    charts: List[Chart]
    insights: List[str]
    metadata: DashboardMetadata


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
