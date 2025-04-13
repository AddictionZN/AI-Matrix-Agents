########################################
# File: prompt_resource_planning.py
########################################
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

"""
Resource Planning Prompt and Schema
-----------------------------------

Use this module to define the Pydantic models, output parser, and system/human prompts
for generating resource allocations (similar to the roles, hours, rates, etc. shown
in your Excel sheet). This approach follows the same pattern as your existing
prompt_cash_flow.py and prompt_cost_estatimations.py.
"""


class ResourceRow(BaseModel):
    """
    Represents a single row in the resource planning table:
    - role: The job title or role.
    - number_of_people: How many people are assigned to this role.
    - hours: Total hours allocated for each person in this role.
    - rate: Hourly or daily rate for each person in this role.
    - total: Calculated total cost (hours * rate * number_of_people).
    """
    role: str = Field(..., description="Title or designation of the resource (e.g., Product Manager).")
    number_of_people: int = Field(..., description="How many people are filling this role.")
    hours: float = Field(..., description="Number of hours allocated per person.")
    rate: float = Field(..., description="Rate per hour (or day) for the role.")
    total: float = Field(..., description="Total cost calculated = hours * rate * number_of_people.")


class ResourcePlanningSheet(BaseModel):
    """
    Represents a resource planning category or sheet, similar to 'Product Development', 'Product IT', etc.
    Each sheet has multiple rows and a subtotal.
    """
    category_name: str = Field(..., description="Name of the category or section (e.g., 'Product IT').")
    rows: List[ResourceRow] = Field(..., description="List of resource rows under this category.")
    category_total: float = Field(..., description="Total cost for this category (sum of all row totals).")


class ResourcePlanning(BaseModel):
    """
    Defines the overall resource planning structure, reflecting the Excel layout in your screenshots.
    """
    project_name: str = Field(..., description="Name of the project or initiative.")
    resource_sheets: List[ResourcePlanningSheet] = Field(..., description="A list of resource sheets/categories.")
    grand_total: float = Field(..., description="Grand total of all categories combined.")
    assumptions: Optional[Dict[str, Any]] = Field(
        None,
        description="Any financial or project assumptions (e.g., duration, WACC, escalations)."
    )


# Create an output parser instance to enforce the JSON schema above.
output_parser = PydanticOutputParser(pydantic_object=ResourcePlanning)

# Define the system prompt that instructs how to generate resource planning data.
RESOURCE_PLANNING_SYSTEM_PROMPT = (
    "You are a resource planning expert specialized in analyzing and generating resource allocations for projects "
    "in a format similar to Excel. IMPORTANT: Before creating any resource plan, you MUST use the available tools to "
    "gather typical roles, rates, hours, and relevant industry benchmarks. Do not rely solely on your internal knowledge. "
    "Use these tools as follows: "
    "- Use the bing_search tool for general industry trends, standard role definitions, and typical rates. "
    "- Use the yahoo_finance_market_data tool to retrieve financial metrics that might inform resource costs. "
    "- Use the yahoo_finance_financials tool for analyzing actual cost structures from comparable companies. "
    "- Use the yahoo_market_sizing tool to understand market position which may impact required resources. "
    "- Use the yahoo_industry_peers tool to compare resource allocations across similar projects in the same industry. "
    "Your final output must adhere to the given JSON schema exactly, reflecting each category (like a sheet), multiple roles, "
    "and a grand total. Include any relevant assumptions (like WACC, escalation rates, or project duration) in the 'assumptions' field."
)

# Template for the human prompt that collects minimal info and instructs the agent to produce a resource plan.
RESOURCE_PLANNING_PROMPT_TEMPLATE = (
    "Generate a comprehensive resource plan for the project '{project_name}'. "
    "Please detail the resource categories (e.g., Product Development, IT Support), each role (with number of people, hours, and rate), "
    "and calculate the total cost per category. Then provide a grand total across all categories. "
    "Additionally, list any important assumptions (such as project duration, cost escalation rates, etc.). "
    "Use the following JSON schema exactly: {format_instructions}"
)

def get_resource_planning_prompt(
    project_name: str,
    additional_context: Optional[str] = None
) -> str:
    """
    Build and return the final prompt for resource planning generation.
    """
    additional_context = additional_context or "No additional context provided."
    format_instructions = output_parser.get_format_instructions()
    prompt = RESOURCE_PLANNING_PROMPT_TEMPLATE.format(
        project_name=project_name,
        format_instructions=format_instructions
    )
    return f"{prompt}\n\nAdditional Context: {additional_context}"
