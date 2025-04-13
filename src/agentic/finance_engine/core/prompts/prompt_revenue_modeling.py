from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser


class RevenueStrategy(BaseModel):
    model_name: str = Field(..., description="Name of the revenue model (e.g., 'Subscription').")
    description: str = Field(..., description="Brief explanation of the revenue model.")
    monthly_revenue_projection: List[float] = Field(
        ..., description="Monthly revenue projections (e.g., for 5 months)."
    )
    total_revenue: float = Field(..., description="Total revenue over the projection period.")


class RevenueModelOutput(BaseModel):
    project_name: str = Field(..., description="Project name.")
    strategies: List[RevenueStrategy] = Field(..., description="List of revenue strategies.")
    recommended_strategy: str = Field(..., description="The recommended revenue strategy.")
    notes: Optional[str] = Field(None, description="Additional notes or considerations.")


# Create an output parser to enforce the JSON schema.
output_parser = PydanticOutputParser(pydantic_object=RevenueModelOutput)

REVENUE_MODELING_SYSTEM_PROMPT: str = (
    "You are a revenue modeling expert. Gather current market data, pricing strategies, and financial benchmarks using available tools. "
    "Provide multiple revenue strategies with monthly projections (for 5 months), compute totals, and recommend a viable strategy with rationale. "
    "Return valid JSON strictly following the provided schema."
)

REVENUE_MODELING_PROMPT_TEMPLATE: str = (
    "Generate a comprehensive revenue model for the project '{project_name}'.\n\n"
    "Steps:\n"
    "1. Include multiple revenue strategies (e.g., 'Base Price + Tier', 'Price per Click', 'Subscription', 'Bundle Pricing', 'Penetration Pricing').\n"
    "2. For each strategy, provide monthly revenue projections for 5 months and calculate the total revenue.\n"
    "3. Recommend one strategy with an explanation of the rationale.\n\n"
    "Return the result as valid JSON following this schema:\n{format_instructions}"
)


def get_revenue_modeling_prompt(
    project_name: str, 
    additional_context: Optional[str] = None
) -> str:
    """
    Build and return the revenue modeling prompt.

    Args:
        project_name: Name of the project.
        additional_context: Optional context; defaults to a generic message if not provided.

    Returns:
        A formatted prompt string.
    """
    context = additional_context or "No additional context provided."
    format_instructions = output_parser.get_format_instructions()
    prompt = REVENUE_MODELING_PROMPT_TEMPLATE.format(
        project_name=project_name,
        format_instructions=format_instructions
    )
    return f"{prompt}\n\nAdditional Context: {context}"
