import logging
from typing import Dict, Any, Optional, List

from base_agent import BaseAgent
from prompts.prompt_resource_planning import (
    RESOURCE_PLANNING_SYSTEM_PROMPT,
    get_resource_planning_prompt
)

# Example tool imports if they exist in your codebase:
from tools.bing_search import bing_search
from tools.yahoo_finance import (
    yahoo_finance_market_data,
    yahoo_finance_financials,
    yahoo_market_sizing,
    yahoo_industry_peers
)

logger = logging.getLogger(__name__)


class ResourcePlanningAgent(BaseAgent):
    """
    An agent specialized in generating resource plans, including roles, hours, rates, and totals
    in an Excel-like structure, along with any relevant assumptions.
    """

    def get_tools(self) -> List:
        """
        Return a list of tools used for gathering market data, role definitions, and cost benchmarks.
        """
        logger.info("Registering tools with ResourcePlanningAgent")
        return [
            bing_search,
            yahoo_finance_market_data,
            yahoo_finance_financials,
            yahoo_market_sizing,
            yahoo_industry_peers
        ]

    def get_system_prompt(self) -> str:
        """
        Return the specialized system prompt for resource planning.
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
        Format the input for the resource planning agent. 

        Note:
          - project_description and industry are inherited from BaseAgent
            but not necessarily used here. You can use them if relevant.
        """
        logger.info(f"Creating resource planning prompt for project: {project_name}")
        return get_resource_planning_prompt(project_name, additional_context)


def generate_resource_plan(
    project_name: str,
    additional_context: Optional[str] = None,
    streaming: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to create a resource plan for the given project.

    Args:
        project_name (str): Name of the project.
        additional_context (Optional[str]): Any extra details or constraints.
        streaming (bool): Whether to stream the output from the language model.

    Returns:
        Dict[str, Any]: Generated resource plan.
    """
    agent = ResourcePlanningAgent(streaming=streaming)
    return agent.generate(
        project_name=project_name,
        project_description="",
        industry="",
        additional_context=additional_context
    )
