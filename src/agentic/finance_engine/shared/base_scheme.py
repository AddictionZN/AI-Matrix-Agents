from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class AdditionalContext(BaseModel):
    """
    Structured model for additional context information.
    """
    market_size: Optional[str] = Field(None, description="Target market size")
    timeframe: Optional[str] = Field(None, description="Project timeframe")
    financial_goals: Optional[str] = Field(None, description="Financial goals and targets")
    initial_investment: Optional[str] = Field(None, description="Available initial investment")
    project_scale: Optional[str] = Field(
        None, description="Scale of the project (Small, Medium, Large)"
    )
    other_details: Optional[Dict[str, Any]] = Field(
        None, description="Any other relevant information"
    )

    class Config:
        extra = "allow"


class BaseFinancialRequest(BaseModel):
    """
    Base model with common fields for all financial analysis requests.
    """
    project_name: str = Field(..., description="Name of the project")
    project_description: str = Field(..., description="Brief description of the project")
    industry: str = Field(..., description="Industry sector of the project")
    additional_context: Optional[
        Union[AdditionalContext, Dict[str, Any]]
    ] = Field(None, description="Additional contextual information for the analysis")

    class Config:
        schema_extra = {
            "example": {
                "project_name": "EcoTech Smart Home System",
                "project_description": "IoT-based smart home system focused on energy efficiency and sustainability",
                "industry": "Consumer Electronics",
                "additional_context": {
                    "market_size": "$50 billion annually",
                    "timeframe": "24 months",
                    "financial_goals": "Break-even within 18 months",
                    "initial_investment": "$750,000",
                    "project_scale": "Medium"
                }
            }
        }
