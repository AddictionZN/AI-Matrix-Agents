from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser


class KeyMetrics(BaseModel):
    wacc: str = Field(..., description="Weighted Average Cost of Capital")
    irr: str = Field(..., description="Internal Rate of Return")
    npv: str = Field(..., description="Net Present Value")
    break_even: str = Field(..., description="Break-Even Period")


class CashFlowTable(BaseModel):
    category: str
    month1: str
    month2: str
    month3: str
    month4: str
    months: str
    total: str


class CashFlowProjection(BaseModel):
    project_name: str
    key_metrics: KeyMetrics
    cash_inflows: List[CashFlowTable]
    cash_outflows: List[CashFlowTable]
    net_flow: List[CashFlowTable]
    additional_notes: str

# Create an output parser instance based on the defined Pydantic model.
output_parser = PydanticOutputParser(pydantic_object=CashFlowProjection)


# Define the system prompt.
CASH_FLOW_SYSTEM_PROMPT = (
    "You are a financial analysis expert specialized in creating comprehensive cash flow projections. "
    "IMPORTANT: Before creating any financial projections, you MUST use the available tools to gather current "
    "market data, industry benchmarks, and relevant financial information. Do not rely solely on your internal knowledge. "
    "In this task, use these tools in the following way: "
    "- Use the bing_search tool for general industry trends, news, and market conditions. "
    "- Use the yahoo_finance_market_data tool to retrieve financial metrics and valuation data for specific companies. "
    "- Use the yahoo_finance_financials tool to analyze actual financial statements from comparable companies. "
    "- Use the yahoo_market_sizing tool to understand market position and growth metrics. "
    "- Use the yahoo_industry_peers tool to compare companies against competitors in the same sector. "
    "Your analysis should be based on the most up-to-date information about the industry and similar projects. "
    "Only after gathering this information should you produce a detailed and realistic cash flow analysis. "
    "Return the final result as valid JSON following the provided schema."
)

# Define the human prompt template.
CASH_FLOW_TEMPLATE = (
    "Generate a cash flow projection for the project '{project_name}' in the {industry} industry. "
    "Project Description: {project_description}. "
    "Additional Context: {additional_context}. "
    "Follow these steps for your analysis: "
    "1. Use the bing_search tool to research current {industry} industry trends, typical project costs, and revenue patterns. "
    "Ensure that all numerical values are realistic and consistent. "
    "Output the result as valid JSON following this schema: {format_instructions}"
)

def get_cash_flow_prompt_prompt(
    project_name: str,
    project_description: str,
    industry: str,
    additional_context: Optional[str] = None
) -> str:
    """
    Build and return the human prompt for the cash flow projection.

    Args:
        project_name (str): Name of the project.
        project_description (str): Description of the project.
        industry (str): Industry sector.
        additional_context (Optional[str]): Additional context.

    Returns:
        str: The formatted human prompt.
    """
    additional_context = additional_context or "No additional context provided"
    format_instructions = output_parser.get_format_instructions()
    prompt = CASH_FLOW_TEMPLATE.format(
        project_name=project_name,
        project_description=project_description,
        industry=industry,
        additional_context=additional_context,
        format_instructions=format_instructions
    )
    return prompt
