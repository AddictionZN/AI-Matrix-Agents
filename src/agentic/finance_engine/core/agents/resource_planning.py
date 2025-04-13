import logging
from typing import Dict, Any, Optional, List
from base_agent import BaseAgent
from prompts.prompt_resource_planning import (
    RESOURCE_PLANNING_SYSTEM_PROMPT,
    get_resource_planning_prompt
)

from tools.yahoo_finance import (
    yahoo_finance_market_data,
    yahoo_finance_financials,
    yahoo_market_sizing,
    yahoo_industry_peers
)

logger = logging.getLogger(__name__)

class ResourcePlanningAgent(BaseAgent):
    """
    Agent specialized in generating a resource plan (roles, hours, rates, totals)
    in an Excel-like structure, along with relevant assumptions (WACC, exchange rates, etc.).
    """

    def get_tools(self) -> List:
        """
        Return a list of tools for data gathering about typical roles, rates,
        and industry benchmarks. Override if additional tools are needed.
        """
        logger.info("Registering tools for ResourcePlanningAgent.")
        return [
            yahoo_finance_market_data,
            yahoo_finance_financials,
            yahoo_market_sizing,
            yahoo_industry_peers
        ]

    def get_system_prompt(self) -> str:
        """
        System prompt guiding the LLM on how to generate resource plans.
        """
        return RESOURCE_PLANNING_SYSTEM_PROMPT

    def _format_input(
        self,
        project_name: str,
        project_description: str,
        industry: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Format the input for the agent. The BaseAgent requires a signature with
        project_name, project_description, and industry, though they may not
        be used if not needed.
        """
        logger.info(f"Creating resource planning prompt for project: {project_name}.")
        return get_resource_planning_prompt(project_name, additional_context)


def generate_resource_plan(
    project_name: str,
    additional_context: Optional[str] = None,
    streaming: bool = False
) -> Dict[str, Any]:
    """
    High-level function to create a resource plan with minimal boilerplate.

    Args:
        project_name (str): The project name.
        additional_context (Optional[str]): Additional context or instructions.
        streaming (bool): Whether to stream the output from the model.

    Returns:
        Dict[str, Any]: The generated resource plan, including 'output', 'success', etc.
    """
    agent = ResourcePlanningAgent(streaming=streaming)
    return agent.generate(
        project_name=project_name,
        project_description="",
        industry="",
        additional_context=additional_context
    )
