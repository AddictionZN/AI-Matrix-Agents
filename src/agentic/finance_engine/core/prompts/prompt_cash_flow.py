from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

class KeyMetrics(BaseModel):
    """
    Represents the key financial metrics that appear at the top of the Excel sheet.
    """
    wacc: str = Field(..., description="Weighted Average Cost of Capital (e.g., '15%').")
    irr: str = Field(..., description="Internal Rate of Return (e.g., '26%').")
    npv: str = Field(..., description="Net Present Value (e.g., '29,442').")
    break_even: str = Field(..., description="Break-Even Period (e.g., '3.17').")

class CashFlowTable(BaseModel):
    """
    Mirrors each row of the cash flow table, with columns for months 1 through 5 and a total.
    """
    category: str = Field(..., description="Category or line item, e.g., 'Total Revenue', 'Initial Investment'.")
    month1: str = Field(..., description="Amount for month 1.")
    month2: str = Field(..., description="Amount for month 2.")
    month3: str = Field(..., description="Amount for month 3.")
    month4: str = Field(..., description="Amount for month 4.")
    month5: str = Field(..., description="Amount for month 5.")
    total: str = Field(..., description="Total amount across all months.")

class CashFlowProjection(BaseModel):
    """
    Defines the entire cash flow projection, including key metrics and multiple sections (inflows, outflows, net flow).
    """
    project_name: str = Field(..., description="Name of the project.")
    key_metrics: KeyMetrics = Field(..., description="Key financial metrics (WACC, IRR, NPV, Break-Even).")
    cash_inflows: List[CashFlowTable] = Field(..., description="Rows detailing cash inflows by month.")
    cash_outflows: List[CashFlowTable] = Field(..., description="Rows detailing cash outflows by month.")
    net_flow: List[CashFlowTable] = Field(..., description="Rows detailing net cash flow calculations.")
    additional_notes: str = Field(..., description="Any extra context or notes about the projection.")

# Create an output parser instance to enforce the JSON schema above.
output_parser = PydanticOutputParser(pydantic_object=CashFlowProjection)

# System prompt guiding the AI to use tools and produce a cash flow in the specified Excel-like format.
CASH_FLOW_SYSTEM_PROMPT = (
    "You are a financial analysis expert specialized in creating comprehensive cash flow projections. "
    "IMPORTANT: Before creating any financial projections, you MUST use the available tools to gather current "
    "market data, industry benchmarks, and relevant financial information. Do not rely solely on your internal knowledge. "
    "Use the following tools in this manner: "
    "- Use the bing_search tool for general industry trends, news, and market conditions. "
    "- Use the yahoo_finance_market_data tool to retrieve financial metrics and valuation data for specific companies. "
    "- Use the yahoo_finance_financials tool to analyze actual financial statements from comparable companies. "
    "- Use the yahoo_market_sizing tool to understand market position and growth metrics. "
    "- Use the yahoo_industry_peers tool to compare companies against competitors in the same sector. "
    "Your analysis must closely match the Excel-style layout with columns for Month 1 through Month 5, "
    "plus a total for each row of inflows and outflows, key metrics at the top, and a final net flow calculation. "
    "Return the final result as valid JSON following the provided schema."
)


CASH_FLOW_TEMPLATE = (
    "Generate a cash flow projection for the project '{project_name}' in the {industry} industry. "
    "Project Description: {project_description}. "
    "Additional Context: {additional_context}. "
    "Use the following steps for your analysis: "
    "1. Research current {industry} industry trends, typical project costs, and revenue patterns using the bing_search tool. "
    "2. If applicable, use Yahoo Finance tools to gather real financial data for relevant companies. "
    "3. Include key metrics (WACC, IRR, NPV, Break-Even) and a table with columns for Month 1 through Month 5, plus a Total. "
    "4. Separate the cash inflows, cash outflows, and net flow. "
    "Ensure all numeric values are realistic and consistent. "
    "Output your result as valid JSON that follows this schema exactly: {format_instructions}"
)

def get_cash_flow_prompt(
    project_name: str,
    project_description: str,
    industry: str,
    additional_context: Optional[str] = None
) -> str:
    """
    Build and return the human-readable prompt for the cash flow projection, specifying five months and a total column.

    Args:
        project_name (str): The name of the project.
        project_description (str): A brief description of the project.
        industry (str): The industry in which the project operates.
        additional_context (Optional[str]): Extra context or details to include in the analysis.

    Returns:
        str: The fully formatted prompt.
    """
    additional_context = additional_context or "No additional context provided"
    format_instructions = output_parser.get_format_instructions()
    return CASH_FLOW_TEMPLATE.format(
        project_name=project_name,
        project_description=project_description,
        industry=industry,
        additional_context=additional_context,
        format_instructions=format_instructions
    )
