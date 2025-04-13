from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser


class KeyMetrics(BaseModel):
    wacc: str = Field(..., description="Weighted Average Cost of Capital (e.g., '15%').")
    irr: str = Field(..., description="Internal Rate of Return (e.g., '26%').")
    npv: str = Field(..., description="Net Present Value (e.g., '29,442').")
    break_even: str = Field(..., description="Break-Even Period (e.g., '3.17').")


class CashFlowTable(BaseModel):
    category: str = Field(..., description="Line item category.")
    month1: str = Field(..., description="Amount for Month 1.")
    month2: str = Field(..., description="Amount for Month 2.")
    month3: str = Field(..., description="Amount for Month 3.")
    month4: str = Field(..., description="Amount for Month 4.")
    month5: str = Field(..., description="Amount for Month 5.")
    total: str = Field(..., description="Total amount over five months.")


class CashFlowProjection(BaseModel):
    project_name: str = Field(..., description="Project name.")
    key_metrics: KeyMetrics = Field(..., description="Key financial metrics.")
    cash_inflows: List[CashFlowTable] = Field(..., description="Cash inflow rows.")
    cash_outflows: List[CashFlowTable] = Field(..., description="Cash outflow rows.")
    net_flow: List[CashFlowTable] = Field(..., description="Net cash flow rows.")
    additional_notes: str = Field(..., description="Extra notes or assumptions.")


# Create an output parser to enforce the JSON schema.
output_parser = PydanticOutputParser(pydantic_object=CashFlowProjection)

# System prompt description for context.
CASH_FLOW_SYSTEM_PROMPT: str = (
    "You are a financial analysis expert specializing in cash flow projections. "
    "Gather relevant market data and financial metrics before generating the projection. "
    "Format the output as an Excel-like table with columns for Month 1 to Month 5 and a Total. "
    "Return valid JSON adhering strictly to the provided schema."
)

# Template used for building the cash flow prompt.
CASH_FLOW_PROMPT_TEMPLATE: str = (
    "Generate a cash flow projection for the project '{project_name}'.\n\n"
    "Project Description: {project_description}\n"
    "Additional Context: {additional_context}\n\n"
    "Steps:\n"
    "1. Research industry trends and relevant market data.\n"
    "2. Determine key financial metrics (WACC, IRR, NPV, Break-Even).\n"
    "3. Construct tables for cash inflows, cash outflows, and net flow with monthly breakdowns and totals.\n\n"
    "Return the result as valid JSON following this schema:\n{format_instructions}"
)


def build_cash_flow_prompt(
    project_name: str, 
    project_description: str, 
    additional_context: Optional[str] = None
) -> str:
    """
    Build and return the cash flow projection prompt.

    Args:
        project_name: Name of the project.
        project_description: Brief description of the project.
        additional_context: Optional context; defaults to a generic message if omitted.

    Returns:
        A formatted prompt string.
    """
    context = additional_context or "No additional context provided."
    format_instructions = output_parser.get_format_instructions()
    return CASH_FLOW_PROMPT_TEMPLATE.format(
        project_name=project_name,
        project_description=project_description,
        additional_context=context,
        format_instructions=format_instructions
    )
