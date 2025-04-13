from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser


class CostEstimationItem(BaseModel):
    project_item: str = Field(..., description="Name of the project item.")
    cost_description: str = Field(..., description="Description of the associated cost.")
    quantity: float = Field(..., description="Quantity (units or hours).")
    amount: float = Field(..., description="Calculated cost (quantity multiplied by unit price).")


class CostEstimationBreakdown(BaseModel):
    cost_type: str = Field(..., description="Cost category (e.g., 'Fixed', 'Variable').")
    details: Optional[str] = Field(None, description="Additional details for the category.")
    cost: float = Field(..., description="Total cost for this category.")


class CostEstimation(BaseModel):
    project_name: str = Field(..., description="Project name.")
    company_name: str = Field(..., description="Company name.")
    company_address: str = Field(..., description="Company address.")
    date: str = Field(..., description="Estimation date.")
    expiration_date: str = Field(..., description="Expiration date of the estimation.")
    project_items: List[CostEstimationItem] = Field(..., description="List of cost estimation items.")
    breakdown: List[CostEstimationBreakdown] = Field(..., description="Detailed cost breakdown by category.")
    total_estimated_cost: float = Field(..., description="Total estimated cost for the project.")
    considerations: Optional[str] = Field(None, description="Additional notes or considerations.")


# Create an output parser to enforce the JSON schema.
output_parser = PydanticOutputParser(pydantic_object=CostEstimation)

ESTIMATIONS_SYSTEM_PROMPT: str = (
    "You are a cost estimation expert. Gather current market and pricing data using available tools. "
    "Generate an Excel-like cost estimation output that includes company details, an itemized cost list, "
    "a detailed breakdown, and the total estimated cost. Return valid JSON strictly adhering to the provided schema."
)

ESTIMATIONS_PROMPT_TEMPLATE: str = (
    "Generate a cost estimation for the project '{project_name}'.\n\n"
    "Company Name: {company_name}\n"
    "Company Address: {company_address}\n"
    "Date: {date}\n"
    "Expiration Date: {expiration_date}\n"
    "Additional Context: {additional_context}\n\n"
    "Steps:\n"
    "1. Gather market rates and pricing data.\n"
    "2. Create an itemized table for project items (columns: Project Item, Cost Description, Quantity, Amount).\n"
    "3. Construct a detailed breakdown by category (e.g., Fixed, Variable).\n"
    "4. Calculate the total estimated cost.\n\n"
    "Return the result as valid JSON following this schema:\n{format_instructions}"
)


def build_estimations_prompt(
    project_name: str,
    company_name: str,
    company_address: str,
    date: str,
    expiration_date: str,
    additional_context: Optional[str] = None
) -> str:
    """
    Build and return the cost estimation prompt.

    Args:
        project_name: Name of the project.
        company_name: Name of the company.
        company_address: Address of the company.
        date: Estimation date.
        expiration_date: Expiration date of the estimation.
        additional_context: Optional additional context; defaults to a generic message if omitted.

    Returns:
        A formatted prompt string.
    """
    context = additional_context or "No additional context provided."
    format_instructions = output_parser.get_format_instructions()
    return ESTIMATIONS_PROMPT_TEMPLATE.format(
        project_name=project_name,
        company_name=company_name,
        company_address=company_address,
        date=date,
        expiration_date=expiration_date,
        additional_context=context,
        format_instructions=format_instructions
    )
