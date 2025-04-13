from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser


class ResourceRow(BaseModel):
    role: str = Field(..., description="Job title or role (e.g., 'Product Manager').")
    number_of_people: int = Field(..., description="Number of people in the role.")
    hours: float = Field(..., description="Hours allocated per person.")
    rate: float = Field(..., description="Hourly or daily rate for the role.")
    total: float = Field(..., description="Total cost (hours * rate * number_of_people).")


class ResourcePlanningSheet(BaseModel):
    category_name: str = Field(..., description="Name of the resource category (e.g., 'Product IT').")
    rows: List[ResourceRow] = Field(..., description="List of resource rows under this category.")
    category_total: float = Field(..., description="Subtotal cost for the category.")


class ResourcePlanning(BaseModel):
    project_name: str = Field(..., description="Project or initiative name.")
    resource_sheets: List[ResourcePlanningSheet] = Field(..., description="Resource planning sheets or categories.")
    grand_total: float = Field(..., description="Grand total cost across all categories.")
    assumptions: Optional[Dict[str, Any]] = Field(
        None, description="Additional assumptions (e.g., project duration, market conditions)."
    )


# Create an output parser to enforce the JSON schema.
output_parser = PydanticOutputParser(pydantic_object=ResourcePlanning)

RESOURCE_PLANNING_SYSTEM_PROMPT: str = (
    "You are a resource planning expert. Use available tools to gather data on typical roles, market rates, and industry benchmarks. "
    "Generate a resource plan in an Excel-like format with multiple categories, listing roles with number of people, hours, rates, and computed totals. "
    "Return valid JSON following the provided schema, including any relevant assumptions."
)

RESOURCE_PLANNING_PROMPT_TEMPLATE: str = (
    "Generate a comprehensive resource plan for the project '{project_name}'.\n\n"
    "Steps:\n"
    "1. Include multiple categories (e.g., 'Product Development', 'IT Support').\n"
    "2. For each category, list roles with number of people, allocated hours, rate, and computed total cost.\n"
    "3. Calculate subtotals for each category and a grand total.\n"
    "4. Include any relevant assumptions.\n\n"
    "Return the result as valid JSON following this schema:\n{format_instructions}"
)


def get_resource_planning_prompt(
    project_name: str, 
    additional_context: Optional[str] = None
) -> str:
    """
    Build and return the resource planning prompt.

    Args:
        project_name: Name of the project.
        additional_context: Optional context; if omitted, a default message is used.

    Returns:
        A formatted prompt string.
    """
    context = additional_context or "No additional context provided."
    format_instructions = output_parser.get_format_instructions()
    prompt = RESOURCE_PLANNING_PROMPT_TEMPLATE.format(
        project_name=project_name,
        format_instructions=format_instructions
    )
    return f"{prompt}\n\nAdditional Context: {context}"
