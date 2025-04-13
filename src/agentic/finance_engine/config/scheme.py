from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal
from enum import Enum


class AnalysisType(str, Enum):
    """
    Enum for the type of financial analysis to perform.
    """
    INCOME_STATEMENT = "income_statement"
    CASH_FLOW = "cash_flow"
    RESOURCE_ALLOCATION = "resource_allocation"


# Base model with common fields for all financial analysis requests.
class BaseFinancialRequest(BaseModel):
    """
    Base model with common fields for all financial analysis requests.
    """
    project_name: str = Field(..., description="Name of the project")
    project_description: str = Field(..., description="Brief description of the project")
    industry: str = Field(..., description="Industry sector of the project")
    additional_context: Optional[str] = Field(None, description="Any extra information to consider")


# Specific request models for each endpoint.
class IncomeStatementRequest(BaseFinancialRequest):
    """
    Request model for income statement analysis.
    """
    pass


class CashFlowRequest(BaseFinancialRequest):
    """
    Request model for cash flow analysis.
    """
    pass


class ResourceAllocationRequest(BaseFinancialRequest):
    """
    Request model for resource allocation analysis.
    """
    pass


class FinancialStatementsRequest(BaseFinancialRequest):
    """
    Request model for comprehensive financial statements analysis.
    """
    pass


# Legacy model for backward compatibility.
class FinancialRequest(BaseFinancialRequest):
    """
    Unified request model for all financial analysis requests (legacy).
    """
    analysis_type: AnalysisType = Field(..., description="Type of financial analysis to perform")


# Response models for each endpoint.
class IncomeStatementResponse(BaseModel):
    """
    Response model for income statement analysis.
    """
    project_name: str
    success: bool
    error: Optional[str] = None
    intermediate_steps: Optional[List] = None
    income_statement: Optional[str] = None


class CashFlowResponse(BaseModel):
    """
    Response model for cash flow analysis.
    """
    project_name: str
    success: bool
    error: Optional[str] = None
    intermediate_steps: Optional[List] = None
    cash_flow_projection: Optional[str] = None


class ResourceAllocationResponse(BaseModel):
    """
    Response model for resource allocation analysis.
    """
    project_name: str
    success: bool
    error: Optional[str] = None
    intermediate_steps: Optional[List] = None
    team_structure: Optional[str] = None


class FinancialStatementsResponse(BaseModel):
    """
    Response model for comprehensive financial statements analysis.
    """
    project_name: str
    success: bool
    error: Optional[str] = None
    team_structure: Optional[str] = None
    cash_flow_projection: Optional[str] = None
    income_statement: Optional[str] = None
    intermediate_steps: Optional[Dict[str, List]] = None


# Legacy response model for backward compatibility.
class FinancialResponse(BaseModel):
    """
    Base response model for all financial analysis responses (legacy).
    The actual financial analysis content will be contained in one of these fields based on the analysis_type.
    """
    project_name: str
    analysis_type: AnalysisType
    success: bool
    error: Optional[str] = None
    intermediate_steps: Optional[List] = None
    income_statement: Optional[str] = None
    cash_flow_projection: Optional[str] = None
    team_structure: Optional[str] = None
