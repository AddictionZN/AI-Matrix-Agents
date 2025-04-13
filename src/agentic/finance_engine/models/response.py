from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class EstimationsResponse(BaseModel):
    """Response model for cost estimations."""
    project_name: str
    success: bool
    cost_estimation: Optional[str] = None
    error: Optional[str] = None
    intermediate_steps: Optional[List[Dict[str, Any]]] = None


class CashFlowResponse(BaseModel):
    """Response model for cash flow analysis."""
    project_name: str
    success: bool
    cash_flow_projection: Optional[str] = None
    error: Optional[str] = None
    intermediate_steps: Optional[List[Dict[str, Any]]] = None

class ResourceAllocationResponse(BaseModel):
    """Response model for resource allocation analysis."""
    project_name: str
    success: bool
    team_structure: Optional[str] = None
    error: Optional[str] = None
    intermediate_steps: Optional[List[Dict[str, Any]]] = None


class FinancialAnalysisResponse(BaseModel):
    """Response model for comprehensive financial statements."""
    project_name: str
    success: bool
    team_structure: Optional[str] = None
    cash_flow_projection: Optional[str] = None
    income_statement: Optional[str] = None
    cost_estimation: Optional[str] = None
    error: Optional[str] = None
    intermediate_steps: Optional[List[Dict[str, Any]]] = None
