from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser


class CostEstimationItem(BaseModel):
    """
    Represents a single line item in the cost estimation, mirroring one row in the Excel table.
    """
    project_item: str = Field(..., description="Name of the project item.")
    cost_description: str = Field(..., description="Description of the associated cost.")
    quantity: float = Field(..., description="Quantity for the item (e.g., units, hours).")
    amount: float = Field(..., description="Total cost calculated as quantity multiplied by unit price.")


class CostEstimationBreakdown(BaseModel):
    """
    Represents a cost breakdown category similar to Excel grouping (e.g., Fixed, Variable, Additional).
    """
    cost_type: str = Field(..., description="Cost category (e.g., 'Fixed', 'Variable', 'Additional').")
    details: Optional[str] = Field(None, description="Additional details for this cost category.")
    cost: float = Field(..., description="Total cost for this category.")


class CostEstimation(BaseModel):
    """
    Defines the overall cost estimation structure reflecting the Excel table layout.
    """
    company_name: str = Field(..., description="Name of the company or client.")
    company_address: str = Field(..., description="Address of the company or client.")
    date: str = Field(..., description="Date of the estimation.")
    expiration_date: str = Field(..., description="Expiration date of the estimate.")
    project_items: List[CostEstimationItem] = Field(
        ..., description="List of cost items matching the Excel table rows."
    )
    breakdown: List[CostEstimationBreakdown] = Field(
        ..., description="Breakdown of costs by category (e.g., Fixed, Variable, Additional)."
    )
    total_estimated_cost: float = Field(..., description="Total estimated cost for the project.")
    considerations: Optional[str] = Field(
        None, description="Additional notes or considerations from the estimation."
    )


# Create an output parser instance to ensure the generated JSON adheres to the ExcelCostEstimation schema.
output_parser = PydanticOutputParser(pydantic_object=CostEstimation)

# Define the system prompt with instructions to gather market data and generate the output in an Excel-like layout.
ESTIMATIONS_SYSTEM_PROMPT = (
    "You are a cost estimation expert specialized in summarizing project budgets. "
    "IMPORTANT: Before creating any cost estimations, you MUST use the available tools to gather current market rates, "
    "pricing data, and industry benchmarks. Do not rely solely on your internal knowledge. "
    "Use these tools as follows: "
    "- Use the bing_search tool for general industry trends, news, and market conditions. "
    "- Use the yahoo_finance_market_data tool to retrieve financial metrics and valuation data for specific companies. "
    "- Use the yahoo_finance_financials tool to analyze actual financial statements from comparable companies. "
    "- Use the yahoo_market_sizing tool to understand market position and growth metrics. "
    "- Use the yahoo_industry_peers tool to compare companies against competitors in the same sector. "
    "Your output should mimic an Excel table layout with the following sections: "
    "1. Company Information (Company Name, Company Address, Date, Expiration Date). "
    "2. A table of cost items with columns: [Project Item, Cost Description, Quantity, Amount]. "
    "3. A cost breakdown by category (e.g., Fixed, Variable, Additional). "
    "4. The total estimated cost and any additional considerations. "
    "Return the final result as valid JSON following the provided schema without any extra commentary."
)

# Define the human prompt template that aligns with the Excel layout.
ESTIMATIONS_PROMPT_TEMPLATE = (
    "Company Name: {company_name}\n"
    "Company Address: {company_address}\n"
    "Date: {date}\n"
    "Expiration Date: {expiration_date}\n"
    "Considerations: {considerations}\n\n"
    "Steps for your analysis:\n"
    "1. Use the bing_search tool to research current market rates, pricing, and cost benchmarks.\n"
    "2. Use yahoo_finance tools to collect financial data from comparable companies if applicable.\n"
    "3. Use yahoo_industry_peers to identify relevant competitors or industry benchmarks.\n"
    "4. Based on the gathered data, construct an Excel-like table with the following layout:\n"
    "   - A table of cost items with columns [Project Item, Cost Description, Quantity, Amount].\n"
    "   - A detailed breakdown by cost category (Fixed, Variable, Additional).\n"
    "   - The total estimated cost for the project.\n"
    "   - Any additional considerations.\n\n"
    "Use the following JSON schema exactly: {format_instructions}"
)


def get_estimations_template_prompt(
    company_name: str,
    company_address: str,
    date: str,
    expiration_date: str,
    considerations: Optional[str] = None
) -> str:
    """
    Builds and returns the complete human prompt for generating an Excel-like cost estimation.

    Args:
        company_name (str): Name of the company or client.
        company_address (str): Address of the company or client.
        date (str): Date of the estimation.
        expiration_date (str): Expiration date of the estimate.
        considerations (Optional[str]): Additional notes or context.

    Returns:
        str: The fully formatted human prompt with all instructions and JSON schema details.
    """
    considerations = considerations or "No additional considerations provided."
    format_instructions = output_parser.get_format_instructions()
    return ESTIMATIONS_PROMPT_TEMPLATE.format(
        company_name=company_name,
        company_address=company_address,
        date=date,
        expiration_date=expiration_date,
        considerations=considerations,
        format_instructions=format_instructions
    )
