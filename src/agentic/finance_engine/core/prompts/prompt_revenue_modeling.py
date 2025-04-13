from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

class RevenueStrategy(BaseModel):
    """
    Represents a specific revenue model or strategy, including its name,
    a brief description or assumptions, and potential monthly revenue projections.
    """
    model_name: str = Field(..., description="Name of the revenue model (e.g., 'Price per Click').")
    description: str = Field(..., description="A brief description of how this model works.")
    monthly_revenue_projection: List[float] = Field(
        ...,
        description="A list of monthly revenue projections (e.g., for 5 months)."
    )
    total_revenue: float = Field(..., description="Sum of the projected monthly revenues.")


class RevenueModelOutput(BaseModel):
    """
    Overall structure containing multiple revenue strategies for a project,
    along with a recommended approach or final conclusion.
    """
    project_name: str = Field(..., description="Name of the project.")
    strategies: List[RevenueStrategy] = Field(..., description="List of possible revenue models.")
    recommended_strategy: str = Field(..., description="A recommendation on which strategy to pursue and why.")
    notes: Optional[str] = Field(None, description="Any additional notes or considerations.")


# Create an output parser to enforce the JSON schema.
output_parser = PydanticOutputParser(pydantic_object=RevenueModelOutput)

# System prompt providing high-level guidance for revenue modeling.
REVENUE_MODELING_SYSTEM_PROMPT = (
    "You are a revenue modeling and pricing strategy expert. You MUST gather current pricing strategies, "
    "industry benchmarks, and relevant financial data using the provided tools before generating revenue models. "
    "Use the following tools in this manner: "
    "- Use the bing_search tool to understand market conditions, typical pricing strategies, and consumer behavior. "
    "- Use the yahoo_finance_market_data tool for any publicly available pricing or revenue data. "
    "- Use the yahoo_finance_financials tool to benchmark against actual financials of comparable companies. "
    "- Use the yahoo_market_sizing tool for overall market size and potential. "
    "- Use the yahoo_industry_peers tool to see how competitors structure their revenue streams. "
    "Your final output must be valid JSON following the schema exactly. Provide multiple revenue strategies, "
    "their monthly projections for up to 5 months, and a final recommended strategy."
)

# Template for the human prompt that will request a revenue modeling plan.
REVENUE_MODELING_PROMPT_TEMPLATE = (
    "Generate a comprehensive set of revenue models for the project '{project_name}'. "
    "Include multiple strategies (such as Base Price + Tier, Price per Click, Subscription, Bundle Pricing, Penetration Pricing) "
    "with monthly revenue projections for 5 months and a total. "
    "Finally, provide your recommendation on which strategy seems most viable, and explain why. "
    "Use the following JSON schema exactly: {format_instructions}"
)


def get_revenue_modeling_prompt(
    project_name: str,
    additional_context: Optional[str] = None
) -> str:
    """
    Build and return the prompt that instructs the model to generate multiple pricing/revenue strategies.
    """
    additional_context = additional_context or "No additional context provided."
    format_instructions = output_parser.get_format_instructions()
    prompt = REVENUE_MODELING_PROMPT_TEMPLATE.format(
        project_name=project_name,
        format_instructions=format_instructions
    )
    return f"{prompt}\n\nAdditional Context: {additional_context}"
