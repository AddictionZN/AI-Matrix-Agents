from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

# Pydantic Models

class EstimationTable(BaseModel):
    """
    Represents a single line item in the cost estimation, similar to one row in Excel.
    """
    project_item: str = Field(..., description="Name of the project or line item.")
    cost_description: str = Field(..., description="Brief description of the cost.")
    quantity: float = Field(..., description="Quantity for the item.")
    amount: float = Field(..., description="Total cost (quantity * unit price).")

class EstimationBreakdown(BaseModel):
    """
    Represents a categorized cost element, e.g., 'Fixed', 'Variable', 'Additional', etc.
    """
    cost_type: str = Field(..., description="Type of cost: 'Fixed', 'Variable', 'Additional', etc.")
    details: Optional[str] = Field(None, description="Any specific details under this cost category.")
    cost: float = Field(..., description="Cost associated with this breakdown entry.")

class EstimationOutput(BaseModel):
    """
    Defines the entire structured cost estimation, reflecting columns and layout from the Excel example.
    """
    company_name: str = Field(..., description="Name of the company or client.")
    company_address: str = Field(..., description="Address of the company or client.")
    date: str = Field(..., description="Date of the estimate.")
    expiration_date: str = Field(..., description="Date when this estimate expires.")
    project_items: List[EstimationTable] = Field(
        ..., description="List of line items reflecting the columns [Project Item, Cost Description, Qty, Amount]."
    )
    breakdown: List[EstimationBreakdown] = Field(
        ..., description="Cost breakdown by category (e.g., Fixed, Variable, Additional)."
    )
    total_estimated_cost: float = Field(..., description="The total estimated project cost.")
    considerations: Optional[str] = Field(
        None, description="Additional considerations or notes from the Excel sheet."
    )

# Create an output parser instance based on the defined Pydantic model.
output_parser = PydanticOutputParser(pydantic_object=EstimationOutput)

# Define the system prompt.
ESTIMATIONS_SYSTEM_PROMPT = (
    "You are a cost estimation expert specialized in summarizing project budgets. "
    "IMPORTANT: Before creating any cost estimations, you MUST use the available tools to gather current "
    "market rates, pricing data, and industry benchmarks. Do not rely solely on your internal knowledge. "
    "Use these tools in the following way: "
    "- Use the bing_search tool for general industry trends, news, and market conditions. "
    "- Use the yahoo_finance_market_data tool to retrieve financial metrics and valuation data for specific companies. "
    "- Use the yahoo_finance_financials tool to analyze actual financial statements from comparable companies. "
    "- Use the yahoo_market_sizing tool to understand market position and growth metrics. "
    "- Use the yahoo_industry_peers tool to compare companies against competitors in the same sector. "
    "Your estimates should be based on the most up-to-date pricing information available. "
    "Reproduce an Excel-like table layout for cost items (columns: Project Item, Cost Description, Qty, Amount), "
    "a breakdown by cost type (e.g., Fixed, Variable, Additional), the total cost, and any notes. "
    "Return the result as valid JSON following the provided schema without extra commentary."
)

# Define the human prompt template.
ESTIMATIONS_TEMPLATE = (
    "Company Name: {company_name}\n"
    "Company Address: {company_address}\n"
    "Date: {date}\n"
    "Expiration Date: {expiration_date}\n"
    "Considerations: {considerations}\n\n"
    "Steps:\n"
    "1. Use the bing_search tool to research current market rates, pricing information, and cost benchmarks.\n"
    "2. Use yahoo_finance tools to find real financial data from comparable companies.\n"
    "3. Use yahoo_industry_peers to identify businesses in the same sector if needed.\n"
    "4. Analyze financial and cost patterns to inform realistic estimations.\n"
    "5. Construct a table matching Excel columns: [Project Item, Cost Description, Qty, Amount], "
    "a cost breakdown by category (Fixed, Variable, Additional), and a final total.\n"
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
    Builds and returns the human prompt for generating an Excel-like cost estimation.

    Args:
        company_name (str): Name of the company or client.
        company_address (str): Address of the company or client.
        date (str): The date of the estimate.
        expiration_date (str): The date when this estimate expires.
        considerations (Optional[str]): Any extra context or details.

    Returns:
        str: A formatted human prompt string containing all instructions and JSON schema details.
    """
    considerations = considerations or "None"
    format_instructions = output_parser.get_format_instructions()
    return ESTIMATIONS_TEMPLATE.format(
        company_name=company_name,
        company_address=company_address,
        date=date,
        expiration_date=expiration_date,
        considerations=considerations,
        format_instructions=format_instructions
    )
